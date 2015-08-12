import unittest
from textmagic.rest import TextmagicRestClient
from textmagic.rest.models import Template
from textmagic import TextmagicException
import time


class TestTemplates(unittest.TestCase):

    template_name = "Test Api Wrapper Template"
    template_body = "Template body"

    template_id = None

    def setUp(self):
        username = "xxx"
        token = "xxx"
        self.client = TextmagicRestClient(username, token)

    def tearDown(self):
        calls = [
            [self.client.templates, self.template_id],
        ]
        for f in calls:
            try:
                time.sleep(.5)
                method = getattr(f[0], "delete")
                method(f[1])
            except:
                continue

    def test_mono_example(self):

        # Create a template

        time.sleep(.5)
        template = self.client.templates.create(
            name=self.template_name,
            content=self.template_body,
        )
        self.template_id = template.id

        self.assertTrue(isinstance(template, Template))
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "href"))

        # Get a template

        time.sleep(.5)
        template = self.client.templates.get(template.id)
        self.assertTrue(isinstance(template, Template))
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "name"))
        self.assertTrue(hasattr(template, "content"))
        self.assertTrue(hasattr(template, "lastModified"))
        self.assertEqual(template.name, self.template_name)
        self.assertEqual(template.content, self.template_body)

        # Update a template

        time.sleep(.5)
        template = self.client.templates.update(
            template.id,
            name="Updated Template",
            content=template.content
        )
        self.assertTrue(isinstance(template, Template))
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "href"))

        # Get an updated template

        time.sleep(.5)
        template = self.client.templates.get(template.id)
        self.assertTrue(isinstance(template, Template))
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "name"))
        self.assertTrue(hasattr(template, "content"))
        self.assertTrue(hasattr(template, "lastModified"))
        self.assertEqual(template.name, "Updated Template")
        self.assertEqual(template.content, self.template_body)

        # Delete a template

        time.sleep(.5)
        r = self.client.templates.delete(template.id)
        self.assertTrue(r)

        # Get a deleted template

        time.sleep(.5)
        self.assertRaises(TextmagicException, self.client.templates.get, template.id)
