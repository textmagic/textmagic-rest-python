import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import Unsubscriber
import time


class TestUnsubscribers(unittest.TestCase):

    phone = "9999876543"

    list_id = None
    contact_id = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def test_mono_example(self):

        # Unsubscribe a phone number

        time.sleep(.5)
        un = self.client.unsubscribers.create(
            phone=self.phone
        )
        self.assertTrue(isinstance(un, Unsubscriber))
        self.assertTrue(hasattr(un, "id"))
        self.assertTrue(hasattr(un, "href"))

        # Get an unsubscribed phone

        time.sleep(.5)
        un = self.client.unsubscribers.get(un.id)
        self.assertTrue(isinstance(un, Unsubscriber))
        self.assertTrue(hasattr(un, "id"))
        self.assertTrue(hasattr(un, "phone"))
        self.assertTrue(hasattr(un, "firstName"))
        self.assertTrue(hasattr(un, "lastName"))
        self.assertTrue(hasattr(un, "unsubscribeTime"))

        self.assertEqual(un.phone, self.phone)
        self.assertEqual(un.firstName, "Unnamed")
        self.assertEqual(un.lastName, "contact")

        # Get an list of unsubscribers

        time.sleep(.5)
        un_list, pager = self.client.unsubscribers.list()
        self.assertTrue(type(un_list) is list)
        self.assertTrue(isinstance(un_list[0], Unsubscriber))

        self.assertTrue(hasattr(un_list[0], "id"))
        self.assertTrue(hasattr(un_list[0], "phone"))
        self.assertTrue(hasattr(un_list[0], "firstName"))
        self.assertTrue(hasattr(un_list[0], "lastName"))
        self.assertTrue(hasattr(un_list[0], "unsubscribeTime"))

        self.assertTrue(isinstance(pager, dict))
        self.assertTrue("page" in pager)
        self.assertTrue("limit" in pager)
        self.assertTrue("pageCount" in pager)