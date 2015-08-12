import unittest
from mock import patch
from textmagic.rest.models import CustomFields


class TestCustomFields(unittest.TestCase):

    def setUp(self):
        self.resource = CustomFields("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=50,
                page=5,
            )
            mock.assert_called_with({
                "limit": 50,
                "page": 5,
                "search": False
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=100,
                page=10,
                search=True,
            )
            mock.assert_called_with({
                "limit": 100,
                "page": 10,
                "search": False
            })

    def test_create(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(name="Birthday")
            mock.assert_called_with({
                "name": "Birthday"
            })

    def test_update(self):
        with patch.object(self.resource, "update_instance") as mock:
            self.resource.update(123, name="UpdatedField")
            mock.assert_called_with(123, {
                "name": "UpdatedField"
            })

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(999)
            mock.assert_called_with(999)