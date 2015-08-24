import sys
import getopt
from textmagic.rest import TextmagicRestClient

# 2.x-3.x-agnostic raw_input
try:
    input = raw_input
except NameError:
    pass


def usage():
    print(
        """
Usage:
    python app.py [options] [arguments]

Options:
    --help (-h)     Display this help message
    --version (-V)  Display this application version

Available commands:
    send            Send the message.
    show            Show sent messages, inbox messages, contacts, lists.
    info            Account info.
        """
    )


def version():
    print("TextMagic Python APIv2 Demo App version 1.0-dev")


def app(args):

    username = "xxx"
    token = "xxx"
    client = TextmagicRestClient(username=username, token=token)

    def send():
        print("SEND MESSAGE")
        print("============")
        text = input("Text: ")

        phones = ""
        print("Enter phone numbers, separated by [ENTER]. Empty string to break.")
        while True:
            phone = input("Phone: ")
            if phone:
                phones += phone+","
            if not phone and phones:
                phones = phones.rstrip(",")
                break
        print("Sending message to %s" % phones)
        prompt = input("Proceed (y/n)? ")
        if prompt == "y":
            m = client.messages.create(text=text, phones=phones)
            print("Message session %s was sent successfully." % m.id)

    def show(args):
        def pagination(title, method, template, fields):
            page = 1
            while True:
                if page < 0:
                    page = 0
                rows, pager = getattr(client, method).list(page=page)
                print("\n  %s  " % title)
                print("===============")
                print("Page %s of %s\n" % (pager["page"], pager["pageCount"]))
                for r in rows:
                    print(template % tuple(getattr(r, x) for x in fields))

                print("\n1. Next page")
                print("2. Previous page")
                print("3. Exit")
                action = input("Your choice[3]:") or 3

                if action == "1":
                    page += 1
                elif action == "2":
                    page -= 1
                else:
                    break

        if "contacts" in args:
            title = "MY CONTACTS"
            method = "contacts"
            template = "%s | %s %s | %s"
            fields = ("id", "first_name", "last_name", "phone")
            pagination(title, method, template, fields)
        elif "lists" in args:
            title = "LISTS"
            method = "lists"
            template = "%s | %s | %s"
            fields = ("id", "name", "members_count")
            pagination(title, method, template, fields)
        elif "sent" in args:
            title = "SENT MESSAGES"
            method = "messages"
            template = "%s | %s | %s"
            fields = ("id", "receiver", "text")
            pagination(title, method, template, fields)
        elif "inbox" in args:
            title = "RECEIVED MESSAGES"
            method = "replies"
            template = "%s | %s | %s"
            fields = ("id", "sender", "text")
            pagination(title, method, template, fields)
        else:
            print("Usage:\n\tpython app.py show sent|inbox|contacts|lists")

    def info():
        user = client.user.get()
        print("ACCOUNT DETAILS")
        print("===============")
        print("User ID    : %s" % user.id)
        print("First name : %s" % user.first_name)
        print("Last name  : %s" % user.last_name)
        print("Username   : %s" % user.username)
        print("Balance    : %s %s" % (user.balance, user.currency["id"]))
        if user.timezone:
            print("Timezone   : %s" % user.timezone["timezone"])

    if "send" in args:
        send()
    elif "show" in args:
        show(args)
    elif "info" in args:
        info()
    else:
        usage()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hV", ["help", "version", "send", "show", "info"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-V", "--version"):
            version()
            sys.exit()

    app(args)


if __name__ == "__main__":
    main(sys.argv[1:])