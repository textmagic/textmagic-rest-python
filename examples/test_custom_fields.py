import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import CustomField, Contact, List
from textmagic import TextmagicException
import time


class TestCustomFields(unittest.TestCase):

    list_name = "Test Api Wrapper List"
    contact_phone = "999000000"
    field_name_a = "Test Custom A"

    field_a_id = None
    field_b_id = None
    list_id = None
    contact_id = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def tearDown(self):
        calls = [
            [self.client.custom_fields, self.field_a_id],
            [self.client.custom_fields, self.field_b_id],
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

        # Create a custom field

        time.sleep(.5)
        field = self.client.custom_fields.create(name=self.field_name_a)
        self.field_a_id = field.id
        self.assertTrue(isinstance(field, CustomField))
        self.assertTrue(hasattr(field, "id"))
        self.assertTrue(hasattr(field, "href"))

        # Get a custom field

        time.sleep(.5)
        field_a = self.client.custom_fields.get(field.id)
        self.assertTrue(isinstance(field_a, CustomField))
        self.assertTrue(hasattr(field_a, "id"))
        self.assertTrue(hasattr(field_a, "name"))
        self.assertTrue(hasattr(field_a, "createdAt"))
        self.assertEqual(field_a.name, self.field_name_a)

        # Update a custom field

        time.sleep(.5)
        field = self.client.custom_fields.update(
            field_a.id,
            name="Test Custom ABC"
        )
        self.assertTrue(isinstance(field, CustomField))
        self.assertTrue(hasattr(field, "id"))
        self.assertTrue(hasattr(field, "href"))

        # Get an updated custom field

        time.sleep(.5)
        field_a = self.client.custom_fields.get(field.id)
        self.assertTrue(isinstance(field_a, CustomField))
        self.assertTrue(hasattr(field_a, "id"))
        self.assertTrue(hasattr(field_a, "name"))
        self.assertTrue(hasattr(field_a, "createdAt"))
        self.assertEqual(field_a.name, "Test Custom ABC")

        # Create a list to assign contact

        time.sleep(.5)
        my_list = self.client.lists.create(
            name=self.list_name
        )
        self.list_id = my_list.id

        # Create a contact

        time.sleep(.5)
        contact = self.client.contacts.create(
            phone=self.contact_phone,
            lists=my_list.id
        )
        self.contact_id = contact.id

        self.assertTrue(isinstance(contact, Contact))
        self.assertTrue(hasattr(contact, "id"))
        self.assertTrue(hasattr(contact, "href"))

        # Update created contact's custom field value.

        time.sleep(.5)
        updated = self.client.custom_fields.update_value(
            uid=field_a.id,
            contactId=contact.id,
            value="abc",
        )
        self.assertTrue(isinstance(updated, Contact))
        self.assertTrue(hasattr(field, "id"))
        self.assertTrue(hasattr(field, "href"))

        # Get an updated contact

        contact = self.client.contacts.get(contact.id)
        custom_fields = contact.customFields
        self.assertTrue(type(custom_fields) is list)
        self.assertTrue(isinstance(custom_fields[0], dict))
        self.assertTrue("value" in custom_fields[0])
        self.assertTrue("id" in custom_fields[0])
        self.assertTrue("name" in custom_fields[0])
        self.assertTrue("createdAt" in custom_fields[0])
        self.assertEqual(custom_fields[0]["value"], "abc")
        self.assertEqual(custom_fields[0]["id"], field_a.id)
        self.assertEqual(custom_fields[0]["name"], field_a.name)

        # Delete a custom field

        time.sleep(.5)
        r = self.client.custom_fields.delete(field_a.id)
        self.assertTrue(r)

        # Get a deleted custom field

        time.sleep(.5)
        self.assertRaises(TextmagicException, self.client.custom_fields.get, field_a.id)