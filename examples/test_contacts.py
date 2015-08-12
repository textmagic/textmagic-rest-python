import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import Contact, List
from textmagic import TextmagicException
import time


class TestContacts(unittest.TestCase):

    list_name = "Test Api Wrapper List"
    contact_first_name = "John"
    contact_last_name = "Doe"
    contact_phone_a = "999000000"
    contact_phone_b = "999000001"

    contact_a_id = None
    contact_b_id = None
    list_id = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def tearDown(self):
        calls = [
            [self.client.contacts, self.contact_a_id],
            [self.client.contacts, self.contact_b_id],
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

        # Create a list to assign contact

        time.sleep(.5)
        my_list = self.client.lists.create(
            name=self.list_name
        )
        self.list_id = my_list.id

        # Create a contact

        time.sleep(.5)
        contact = self.client.contacts.create(
            firstName=self.contact_first_name,
            lastName=self.contact_last_name,
            phone=self.contact_phone_a,
            lists=my_list.id
        )
        self.contact_a_id = contact.id

        self.assertTrue(isinstance(contact, Contact))
        self.assertTrue(hasattr(contact, "id"))
        self.assertTrue(hasattr(contact, "href"))

        # Get a contact

        time.sleep(.5)
        contact_a = self.client.contacts.get(contact.id)
        self.assertTrue(isinstance(contact_a, Contact))
        self.assertTrue(hasattr(contact_a, "id"))
        self.assertTrue(hasattr(contact_a, "phone"))
        self.assertTrue(hasattr(contact_a, "email"))
        self.assertTrue(hasattr(contact_a, "firstName"))
        self.assertTrue(hasattr(contact_a, "lastName"))
        self.assertTrue(hasattr(contact_a, "companyName"))
        self.assertTrue(hasattr(contact_a, "country"))
        self.assertTrue(isinstance(contact_a.country, dict))
        self.assertTrue(hasattr(contact_a, "customFields"))
        self.assertTrue(type(contact_a.customFields) is list)
        self.assertEqual(contact_a.firstName, self.contact_first_name)
        self.assertEqual(contact_a.lastName, self.contact_last_name)
        self.assertEqual(contact_a.phone, self.contact_phone_a)

        # Create a second contact

        time.sleep(.5)
        contact_b = self.client.contacts.create(
            firstName="James",
            lastName="Smith",
            phone=self.contact_phone_b,
            lists=my_list.id
        )
        self.contact_b_id = contact_b.id

        self.assertTrue(isinstance(contact_b, Contact))
        self.assertTrue(hasattr(contact_b, "id"))
        self.assertTrue(hasattr(contact_b, "href"))

        # Get a contact list

        time.sleep(.5)
        contacts, pager = self.client.contacts.list()
        self.assertTrue(type(contacts) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertTrue("page" in pager)
        self.assertTrue("limit" in pager)
        self.assertTrue("pageCount" in pager)
        self.assertTrue(isinstance(contacts[0], Contact))

        # Search a first contact

        time.sleep(.5)
        contacts, _ = self.client.contacts.list(search=True, query=self.contact_phone_a)

        needle = None
        for c in contacts:
            if c.phone == self.contact_phone_a:
                needle = c

        self.assertTrue(isinstance(needle, Contact))
        self.assertEqual(needle.id, contact_a.id)
        self.assertEqual(needle.phone, contact_a.phone)
        self.assertEqual(needle.firstName, self.contact_first_name)
        self.assertEqual(needle.lastName, self.contact_last_name)

        # Update a first contact

        time.sleep(.5)
        updated = self.client.contacts.update(
            contact_a.id,
            firstName="Boris",
            lastName="The Bullet-Dodger",
            phone=contact_a.phone,
            lists=my_list.id,
        )

        self.assertTrue(isinstance(updated, Contact))
        self.assertTrue(hasattr(updated, "id"))
        self.assertTrue(hasattr(updated, "href"))

        # Get an updated first contact

        time.sleep(.5)
        contact_a = self.client.contacts.get(contact_a.id)
        self.assertTrue(isinstance(contact_a, Contact))
        self.assertEqual(contact_a.firstName, "Boris")
        self.assertEqual(contact_a.lastName, "The Bullet-Dodger")
        self.assertEqual(contact_a.phone, self.contact_phone_a)

        # Get the lists assigned to the contact

        time.sleep(.5)
        lists, pager = self.client.contacts.lists(contact_a.id)
        self.assertTrue(type(lists) is list)
        self.assertTrue(isinstance(pager, dict))
        self.assertEqual(len(lists), 1)
        self.assertTrue(isinstance(lists[0], List))
        self.assertEqual(lists[0].name, self.list_name)

        # Delete a contact

        time.sleep(.5)
        r = self.client.contacts.delete(contact.id)
        self.assertTrue(r)

        # Get a deleted contact

        time.sleep(.5)
        self.assertRaises(TextmagicException, self.client.contacts.get, contact.id)