import unittest
from mock import patch
from textmagic.rest.models import Unsubscribers


class TestUnsubscribers(unittest.TestCase):

    def setUp(self):
        self.resource = Unsubscribers("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=2
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 2,
                "search": False
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=2,
                search=True
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 2,
                "search": False
            })

    def test_create(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(phone="999123456")
            mock.assert_called_with({
                "phone": "999123456"
            })