import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import User, SpendingStat, MessagingStat, Invoice, Number, Senderid, Source
from textmagic import TextmagicException
import time


class TestUsers(unittest.TestCase):

    senderid = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def tearDown(self):
        calls = [
            [self.client.senderids, self.senderid],
        ]
        for f in calls:
            try:
                time.sleep(.5)
                method = getattr(f[0], "delete")
                method(f[1])
            except:
                continue


    def test_mono_example(self):

        # Get a messaging stat

        time.sleep(.5)
        m_stat = self.client.stats_messaging.list()

        self.assertTrue(type(m_stat) is list)
        self.assertTrue(isinstance(m_stat[0], MessagingStat))
        self.assertTrue(hasattr(m_stat[0], "replyRate"))
        self.assertTrue(hasattr(m_stat[0], "date"))
        self.assertTrue(hasattr(m_stat[0], "deliveryRate"))
        self.assertTrue(hasattr(m_stat[0], "costs"))
        self.assertTrue(hasattr(m_stat[0], "messagesReceived"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentDelivered"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentAccepted"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentBuffered"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentFailed"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentRejected"))
        self.assertTrue(hasattr(m_stat[0], "messagesSentParts"))

        # Get a spending stat

        time.sleep(.5)
        s_stat, pager = self.client.stats_spending.list()

        self.assertTrue(type(s_stat) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue("page" in pager)
        self.assertTrue("limit" in pager)
        self.assertTrue("pageCount" in pager)

        # Get invoices

        time.sleep(.5)
        invoices, pager = self.client.invoices.list()

        self.assertTrue(type(invoices) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue(isinstance(invoices[0], Invoice))

        self.assertTrue(hasattr(invoices[0], "id"))
        self.assertTrue(hasattr(invoices[0], "bundle"))
        self.assertTrue(hasattr(invoices[0], "currency"))
        self.assertTrue(hasattr(invoices[0], "vat"))
        self.assertTrue(hasattr(invoices[0], "paymentMethod"))

        # Get numbers list

        time.sleep(.5)
        numbers, pager = self.client.numbers.list()

        self.assertTrue(type(numbers) is list)
        self.assertTrue(isinstance(pager, dict))

        self.assertTrue(isinstance(numbers[0], Number))
        self.assertTrue(hasattr(numbers[0], "id"))
        self.assertTrue(hasattr(numbers[0], "user"))
        self.assertTrue(hasattr(numbers[0], "purchasedAt"))
        self.assertTrue(hasattr(numbers[0], "expireAt"))
        self.assertTrue(hasattr(numbers[0], "phone"))
        self.assertTrue(hasattr(numbers[0], "country"))
        self.assertTrue(hasattr(numbers[0], "status"))

        # Get number

        time.sleep(.5)
        number = self.client.numbers.get(numbers[0].id)

        self.assertTrue(isinstance(number, Number))
        self.assertTrue(hasattr(number, "id"))
        self.assertTrue(hasattr(number, "user"))
        self.assertTrue(hasattr(number, "purchasedAt"))
        self.assertTrue(hasattr(number, "expireAt"))
        self.assertTrue(hasattr(number, "phone"))
        self.assertTrue(hasattr(number, "country"))
        self.assertTrue(hasattr(number, "status"))

        # Get available numbers

        time.sleep(.5)
        available = self.client.numbers.available(country="US", prefix="1646")

        self.assertTrue(isinstance(available, dict))
        self.assertTrue("numbers" in available)
        self.assertTrue(type(available["numbers"]) is list)
        self.assertEqual(available["numbers"][0][:4], "1646")
        self.assertTrue("price" in available)

        # Create Sender ID

        time.sleep(.5)
        senderid = self.client.senderids.create(senderId="TEST", explanation="For testing")
        self.senderid = senderid.id

        self.assertTrue(isinstance(senderid, Senderid))
        self.assertTrue(hasattr(senderid, "id"))
        self.assertTrue(hasattr(senderid, "href"))

        # Get A Sender ID

        time.sleep(.5)
        senderid = self.client.senderids.get(senderid.id)

        self.assertTrue(isinstance(senderid, Senderid))
        self.assertTrue(hasattr(senderid, "id"))
        self.assertTrue(hasattr(senderid, "senderId"))
        self.assertTrue(hasattr(senderid, "user"))
        self.assertTrue(hasattr(senderid, "status"))

        # Get sender IDs list

        time.sleep(.5)
        senderids, pager = self.client.senderids.list()

        self.assertTrue(type(senderids) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue(isinstance(senderids[0], Senderid))
        self.assertTrue(hasattr(senderids[0], "id"))
        self.assertTrue(hasattr(senderids[0], "senderId"))
        self.assertTrue(hasattr(senderids[0], "user"))
        self.assertTrue(hasattr(senderids[0], "status"))

        # Delete a Sender Id

        time.sleep(.5)
        r = self.client.senderids.delete(senderid.id)
        self.assertTrue(r)

        # Get deleted sender id

        self.assertRaises(TextmagicException, self.client.senderids.get, senderid.id)

        # Get allowed froms

        time.sleep(.5)
        allowed = self.client.sources.allowed(country="US")

        self.assertTrue(isinstance(allowed, Source))
        self.assertTrue(hasattr(allowed, "dedicated"))
        self.assertTrue(hasattr(allowed, "shared"))
        self.assertTrue(hasattr(allowed, "senderIds"))

        # Get user info

        time.sleep(.5)
        user = self.client.user.get()

        self.assertTrue(isinstance(user, User))
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "username"))
        self.assertTrue(hasattr(user, "firstName"))
        self.assertTrue(hasattr(user, "lastName"))
        self.assertTrue(hasattr(user, "balance"))
        self.assertTrue(hasattr(user, "currency"))
        self.assertTrue(hasattr(user, "timezone"))
        self.assertTrue(isinstance(user.currency, dict))
        self.assertTrue("id" in user.currency)
        self.assertTrue("htmlSymbol" in user.currency)

        # ! Don't uncomment this if you don't want spend your balance for buying dedicated number !
        # # Buy dedicated number
        #
        # time.sleep(.5)
        # phone = available["numbers"][0]
        # number = self.client.numbers.buy(phone=phone, country="US", userId=user.id)
        #
        # self.assertTrue(isinstance(number, Number))
        # self.assertTrue(hasattr(number, "id"))
        # self.assertTrue(hasattr(number, "href"))
        #
        # # Cancel dedicated number
        #
        # time.sleep(.5)
        # r = self.client.numbers.delete(number.id)
        # self.assertTrue(r)
        #
        # # Get deleted dedicated number
        #
        # self.assertRaises(TextmagicException, self.client.numbers.get, number.id)

        # Update user info

        time.sleep(.5)
        updated = self.client.user.update(
            firstName=user.firstName,
            lastName=user.lastName,
            company=user.company
        )

        # Get subaccounts list

        time.sleep(.5)
        subs, pager = self.client.subaccounts.list()

        self.assertTrue(type(subs) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue(isinstance(subs[0], User))

        # Send invite

        # time.sleep(.5)
        # r = self.client.subaccounts.send_invite(email="qaw@mailinator.com", role="A")
        # self.assertTrue(r)

        # Get subaccount

        time.sleep(.5)
        sub = self.client.subaccounts.get(subs[0].id)

        self.assertTrue(isinstance(sub, User))
        self.assertTrue(hasattr(sub, "id"))
        self.assertTrue(hasattr(sub, "username"))
        self.assertTrue(hasattr(sub, "firstName"))
        self.assertTrue(hasattr(sub, "lastName"))
        self.assertTrue(hasattr(sub, "balance"))
        self.assertTrue(hasattr(sub, "company"))
        self.assertTrue(hasattr(sub, "currency"))
        self.assertTrue(hasattr(sub, "timezone"))
        self.assertTrue(hasattr(sub, "subaccountType"))

        # ! Don't uncomment this because it close one of yours subaccounts !
        # # Close subaccount
        #
        # time.sleep(.5)
        # r = self.client.subaccounts.close(subs[0].id)
        # self.assertTrue(r)

        # Ping

        time.sleep(.5)
        p = self.client.util.ping()

        self.assertTrue(isinstance(p, dict))
        self.assertTrue("ping" in p)
        self.assertEqual(p["ping"], "pong")

