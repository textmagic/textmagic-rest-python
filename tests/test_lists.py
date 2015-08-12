import unittest
from mock import patch, Mock
from textmagic.rest.models import Contacts, Lists


class TestLists(unittest.TestCase):

    def setUp(self):
        self.resource = Lists("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=100,
                page=5,
            )
            mock.assert_called_with({
                "limit": 100,
                "page": 5,
                "search": False
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                search=True,
                limit=100,
                page=5,
                ids="123, 456",
                query="abc",
            )
            mock.assert_called_with({
                "limit": 100,
                "page": 5,
                "search": True,
                "ids": "123, 456",
                "query": "abc"
            })

    def test_create(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(
                name="My List",
                description="My Description",
                shared=0,
            )
            mock.assert_called_with({
                "name": "My List",
                "description": "My Description",
                "shared": 0
            })

    def test_update(self):
        with patch.object(self.resource, "update_instance") as mock:
            self.resource.update(123,
                                 name="My List",
                                 description="List Description",
                                 shared=1)
            mock.assert_called_with(123, {
                "name": "My List",
                "description": "List Description",
                "shared": 1
            })

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(111)
            mock.assert_called_with(111)

    def test_put_contacts(self):
        with patch.object(self.resource, "update_subresource_instance") as mock:
            self.resource.put_contacts(101, contacts="123, 456")

            mock.assert_called_with(101,
                                    body={"contacts": "123, 456"},
                                    slug="contacts",
                                    subresource=None
                                    )

    def test_delete_contacts(self):
        with patch.object(self.resource, "request") as mock:
            mock.return_value = (Mock(status=204), "instance")

            result = self.resource.delete_contacts(123, contacts="999, 888")

            mock.assert_called_with("DELETE",
                                    "%s/%s/contacts" % (self.resource.uri, "123"),
                                    data={"contacts": "999, 888"}
                                    )
            self.assertTrue(result)