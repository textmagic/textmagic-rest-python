import unittest
from mock import patch
from textmagic.rest.models import Templates


class TestTemplates(unittest.TestCase):

    def setUp(self):
        self.resource = Templates("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=1
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 1,
                "search": False,
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=1,
                search=True,
                content="abc abc"
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 1,
                "search": True,
                "content": "abc abc",
            })

    def test_create(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(
                name="template",
                content="template content",
            )
            mock.assert_called_with({
                "name": "template",
                "content": "template content",
            })

    def test_update(self):
        with patch.object(self.resource, "update_instance") as mock:
            self.resource.update(
                123,
                name="updated",
                content="content updated",
            )
            mock.assert_called_with(123, {
                "name": "updated",
                "content": "content updated",
            })

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(999)
            mock.assert_called_with(999)