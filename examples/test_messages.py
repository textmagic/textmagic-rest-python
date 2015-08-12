import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import Message, Session, Schedule, Bulk, ChatMessage, Chat
from textmagic import TextmagicException
import time


username = "xxx"
token = "xxx"


class TestMessages(unittest.TestCase):

    phones = "999000001"
    text = "test api python"

    session_id = None
    scheduled_id = None

    def setUp(self):
        self.client = TextmagicRestClient(username=username, token=token)

    def tearDown(self):
        calls = [
            [self.client.sessions, self.session_id],
            [self.client.schedules, self.scheduled_id],
        ]
        for f in calls:
            try:
                time.sleep(.5)
                method = getattr(f[0], "delete")
                method(f[1])
            except:
                continue

    def test_mono_example(self):

        client = self.client

        # Send a single message

        time.sleep(0.5)
        message = client.messages.create(
            text=self.text,
            phones=self.phones
        )
        self.session_id = message.id

        self.assertTrue(isinstance(message, Message))
        self.assertTrue(hasattr(message, "id"))
        self.assertTrue(hasattr(message, "href"))
        self.assertTrue(hasattr(message, "type"))
        self.assertTrue(hasattr(message, "sessionId"))
        self.assertTrue(hasattr(message, "bulkId"))
        self.assertTrue(hasattr(message, "messageId"))
        self.assertTrue(hasattr(message, "scheduleId"))
        self.assertEqual(message.type, "message")

        # Get a session

        time.sleep(0.5)
        session = client.sessions.get(message.sessionId)

        self.assertTrue(isinstance(session, Session))
        self.assertTrue(hasattr(session, "id"))
        self.assertTrue(hasattr(session, "startTime"))
        self.assertTrue(hasattr(session, "text"))
        self.assertTrue(hasattr(session, "source"))
        self.assertTrue(hasattr(session, "referenceId"))
        self.assertTrue(hasattr(session, "price"))
        self.assertTrue(hasattr(session, "numbersCount"))

        self.assertEqual(self.text, session.text)
        self.assertEqual(session.source, "A")
        self.assertEqual(session.price, 0)
        self.assertEqual(session.numbersCount, 1)

        # Get messages from session

        time.sleep(0.5)
        session_messages, _ = client.sessions.messages(session.id)

        self.assertTrue(type(session_messages) is list)
        self.assertEqual(len(session_messages), 1)
        self.assertTrue(isinstance(session_messages[0], Message))
        self.assertEqual(session_messages[0].text, self.text)

        # Get sessions list

        time.sleep(0.5)
        sessions, pager = client.sessions.list()

        self.assertTrue(type(sessions) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue(isinstance(sessions[0], Session))

        # Get a single message

        time.sleep(0.5)
        single_message = client.messages.get(message.id)

        self.assertTrue(isinstance(single_message, Message))
        self.assertTrue(hasattr(single_message, "id"))
        self.assertTrue(hasattr(single_message, "receiver"))
        self.assertTrue(hasattr(single_message, "messageTime"))
        self.assertTrue(hasattr(single_message, "status"))
        self.assertTrue(hasattr(single_message, "text"))
        self.assertTrue(hasattr(single_message, "charset"))
        self.assertTrue(hasattr(single_message, "firstName"))
        self.assertTrue(hasattr(single_message, "lastName"))
        self.assertTrue(hasattr(single_message, "country"))
        self.assertTrue(hasattr(single_message, "sender"))
        self.assertTrue(hasattr(single_message, "price"))
        self.assertTrue(hasattr(single_message, "partsCount"))

        # Get a messages list

        time.sleep(0.5)
        messages, pager = client.messages.list()

        self.assertTrue(type(session_messages) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue(isinstance(messages[0], Message))

        self.assertTrue(hasattr(messages[0], "id"))
        self.assertTrue(hasattr(messages[0], "receiver"))
        self.assertTrue(hasattr(messages[0], "messageTime"))
        self.assertTrue(hasattr(messages[0], "status"))
        self.assertTrue(hasattr(messages[0], "text"))
        self.assertTrue(hasattr(messages[0], "charset"))
        self.assertTrue(hasattr(messages[0], "firstName"))
        self.assertTrue(hasattr(messages[0], "lastName"))
        self.assertTrue(hasattr(messages[0], "country"))
        self.assertTrue(hasattr(messages[0], "sender"))
        self.assertTrue(hasattr(messages[0], "price"))
        self.assertTrue(hasattr(messages[0], "partsCount"))

        self.assertEqual(messages[0].text, self.text)
        self.assertEqual(messages[0].receiver, self.phones)
        self.assertEqual(messages[0].country, "ZZ")

        # Delete a single message

        time.sleep(0.5)
        r = client.messages.delete(single_message.id)
        self.assertTrue(r)

        # Get a deleted single message

        time.sleep(.5)
        self.assertRaises(TextmagicException, client.messages.get, single_message.id)

        # Delete a session

        time.sleep(0.5)
        r = client.sessions.delete(session.id)
        self.assertTrue(r)

        # Get a deleted session

        time.sleep(.5)
        self.assertRaises(TextmagicException, client.sessions.get, session.id)

        # Create a dummy message

        time.sleep(0.5)
        dummy_message = client.messages.create(text=self.text,
                                               phones=self.phones,
                                               dummy=1)

        self.assertTrue("total" in dummy_message)
        self.assertTrue("parts" in dummy_message)
        self.assertTrue("countries" in dummy_message)

        # Message price

        time.sleep(0.5)
        price = client.messages.price(
            text=self.text,
            phones="99900000"
        )

        self.assertTrue("total" in price)
        self.assertTrue("parts" in price)
        self.assertTrue("countries" in price)

        # Create a scheduled message

        time.sleep(0.5)
        start_time = int(time.time()) + 7200
        message = client.messages.create(text=self.text,
                                         phones=self.phones,
                                         sendingTime=start_time)

        self.scheduled_id = message.id

        self.assertTrue(isinstance(message, Message))
        self.assertTrue(hasattr(message, "id"))
        self.assertTrue(hasattr(message, "href"))
        self.assertTrue(hasattr(message, "type"))
        self.assertTrue(hasattr(message, "sessionId"))
        self.assertTrue(hasattr(message, "bulkId"))
        self.assertTrue(hasattr(message, "messageId"))
        self.assertTrue(hasattr(message, "scheduleId"))
        self.assertEqual(message.type, "schedule")

        # Get a scheduled message

        time.sleep(0.5)
        scheduled = client.schedules.get(message.id)

        self.assertTrue(isinstance(scheduled, Schedule))
        self.assertTrue(hasattr(scheduled, "id"))
        self.assertTrue(hasattr(scheduled, "nextSend"))
        self.assertTrue(hasattr(scheduled, "session"))
        self.assertTrue(hasattr(scheduled, 'rrule'))

        self.assertTrue("id" in scheduled.session)
        self.assertTrue("startTime" in scheduled.session)
        self.assertTrue("text" in scheduled.session)
        self.assertTrue("source" in scheduled.session)
        self.assertTrue("referenceId" in scheduled.session)
        self.assertTrue("price" in scheduled.session)
        self.assertTrue("numbersCount" in scheduled.session)

        # Delete a scheduled message

        time.sleep(0.5)
        r = client.schedules.delete(message.id)
        self.assertTrue(r)

        # Get bulks list

        time.sleep(0.5)
        bulks, pager = client.bulks.list()

        self.assertTrue(type(bulks) is list)
        self.assertTrue(isinstance(pager, dict))

        self.assertTrue(bulks[0], Bulk)
        self.assertTrue(hasattr(bulks[0], "id"))
        self.assertTrue(hasattr(bulks[0], "status"))
        self.assertTrue(hasattr(bulks[0], "itemsProcessed"))
        self.assertTrue(hasattr(bulks[0], "itemsTotal"))
        self.assertTrue(hasattr(bulks[0], "createdAt"))
        self.assertTrue(hasattr(bulks[0], "text"))
        self.assertTrue(hasattr(bulks[0], "session"))

        # Get chat messages by phone

        time.sleep(0.5)
        chat_msgs, pager = client.chats.by_phone('79659750964')

        self.assertTrue(type(chat_msgs) is list)
        self.assertTrue(isinstance(pager, dict))

        self.assertTrue(chat_msgs[0], ChatMessage)
        self.assertTrue(hasattr(chat_msgs[0], "id"))
        self.assertTrue(hasattr(chat_msgs[0], "sender"))
        self.assertTrue(hasattr(chat_msgs[0], "messageTime"))
        self.assertTrue(hasattr(chat_msgs[0], "text"))
        self.assertTrue(hasattr(chat_msgs[0], "receiver"))
        self.assertTrue(hasattr(chat_msgs[0], "status"))
        self.assertTrue(hasattr(chat_msgs[0], "firstName"))
        self.assertTrue(hasattr(chat_msgs[0], "lastName"))

        # Get chat list

        time.sleep(0.5)
        chats, pager = client.chats.list()

        self.assertTrue(type(chats) is list)
        self.assertTrue(isinstance(pager, dict))

        self.assertTrue(isinstance(chats[0], Chat))
        self.assertTrue(hasattr(chats[0], "id"))
        self.assertTrue(hasattr(chats[0], "phone"))
        self.assertTrue(hasattr(chats[0], "contact"))
        self.assertTrue(hasattr(chats[0], "unread"))
        self.assertTrue(hasattr(chats[0], "updatedAt"))