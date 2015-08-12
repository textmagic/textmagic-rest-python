from . import Model, CollectionModel


class ChatMessage(Model):
    """
    A Chat Message object model

    .. attribute:: id

    .. attribute:: direction

    .. attribute:: sender

    .. attribute:: messageTime

    .. attribute:: text

    .. attribute:: receiver

    .. attribute:: deleted

    .. attribute:: userId

    .. attribute:: status

    .. attribute:: total

    .. attribute:: firstName

    .. attribute:: lastName
    """


class ChatMessages(CollectionModel):
    instance = ChatMessage
    name = "chats"
    searchable = False


class Chat(Model):
    """
    A Chat object model

    .. attribute:: id

    .. attribute:: phone

    .. attribute:: contact

        Dictionary like this:
        ::
            {
                "id": 4329702,
                "firstName": "Jonh",
                "lastName": "Doe",
                "companyName": "",
                "phone": "19025555555",
                "email": "",
                "country": {
                    "id": "CA",
                    "name": "Canada"
                },
                "customFields": [
                    {
                        "value": "1970-01-01",
                        "id": 1111,
                        "name": "Birthday",
                        "createdAt": "2015-04-10T06:51:02+0000"
                    }
                ]
            }

    .. attribute:: unread

    .. attribute:: updatedAt
    """


class Chats(CollectionModel):
    name = "chats"
    instance = Chat
    searchable = False

    def list(self, **kwargs):
        """
        Returns a list of :class:`Chat` objects and a pager dict.

        :Example:

        chats, pager = client.chats.list()

        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def by_phone(self, phone=0, **kwargs):
        """
        Fetch messages from chat with specified phone number.

        :Example:

        chat = client.chats.by_phone(phone="447624800500")

        :param str phone: Phone number in E.164 format.
        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        chat_messages = ChatMessages(self.base_uri, self.auth)
        return self.get_subresource_instances(uid=phone, instance=chat_messages, params=kwargs)