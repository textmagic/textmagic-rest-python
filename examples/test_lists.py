import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import Contact, List
from textmagic import TextmagicException
import time


class TestLists(unittest.TestCase):

    list_name = "Test Api Wrapper List"
    contact_phone = "999000000"

    contact_id = None
    list_id = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def tearDown(self):
        calls = [
            [self.client.contacts, self.contact_id],
            [self.client.lists, self.list_id],
        ]
        for f in calls:
            try:
                time.sleep(.5)
                method = getattr(f[0], "delete")
                method(f[1])
            except:
                continue

    def test_mono_example(self):

        # Create a list

        time.sleep(.5)
        l = self.client.lists.create(
            name=self.list_name
        )
        self.list_id = l.id

        self.assertTrue(isinstance(l, List))
        self.assertTrue(hasattr(l, "id"))
        self.assertTrue(hasattr(l, "href"))

        # Get a list

        time.sleep(.5)
        _list = self.client.lists.get(l.id)
        self.assertTrue(isinstance(_list, List))
        self.assertTrue(hasattr(_list, "id"))
        self.assertTrue(hasattr(_list, "name"))
        self.assertTrue(hasattr(_list, "description"))
        self.assertTrue(hasattr(_list, "membersCount"))
        self.assertTrue(hasattr(_list, "shared"))
        self.assertEqual(_list.name, self.list_name)
        self.assertEqual(_list.membersCount, 0)
        self.assertEqual(_list.shared, 0)

        # Update a list

        time.sleep(.5)
        _list = self.client.lists.update(
            _list.id,
            name="Updated Api Wrapper List"
        )

        # Get a list of lists

        time.sleep(.5)
        lists, pager = self.client.lists.list()
        self.assertTrue(type(lists) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue("page" in pager)
        self.assertTrue("limit" in pager)
        self.assertTrue("pageCount" in pager)
        self.assertTrue(isinstance(lists[0], List))

        # Create a contact to assign to list

        time.sleep(.5)
        contact = self.client.contacts.create(
            phone=self.contact_phone,
            lists=_list.id
        )
        self.contact_id = contact.id

        self.assertTrue(isinstance(contact, Contact))
        self.assertTrue(hasattr(contact, "id"))
        self.assertTrue(hasattr(contact, "href"))

        # Get contacts in list

        time.sleep(.5)
        contacts, pager = self.client.lists.contacts(
            _list.id
        )

        self.assertTrue(type(contacts) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue("page" in pager)
        self.assertTrue("limit" in pager)
        self.assertTrue("pageCount" in pager)
        self.assertTrue(isinstance(contacts[0], Contact))

        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].phone, self.contact_phone)

        # Delete a list

        time.sleep(.5)
        r = self.client.lists.delete(_list.id)
        self.assertTrue(r)

        # Get a deleted list

        time.sleep(.5)
        self.assertRaises(TextmagicException, self.client.lists.get, _list.id)