import unittest
from mock import patch, Mock, call
from textmagic.rest.models import Users, MessagingStats, SpendingStats, Utils, Invoices


class TestUser(unittest.TestCase):

    def setUp(self):
        self.resource = Users("uri", ("username", "token"))

    def test_get(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(), "{json instance}")

                self.resource.get()

                mock_request.assert_called_with("GET", self.resource.uri)
                mock_load.assert_called_with("{json instance}")

    def test_update(self):
        with patch.object(self.resource, "request") as mock:
            mock.return_value = (Mock(status=201), "{json instance}")

            result = self.resource.update(
                firstName="John",
                lastName="Doe",
                company="Company",
                timezone=1,
            )
            mock.assert_called_with("PUT", self.resource.uri, data={
                "firstName": "John",
                "lastName": "Doe",
                "company": "Company",
                "timezone": 1,
            })

            self.assertTrue(result)


class TestMessagingStat(unittest.TestCase):

    def setUp(self):
        self.resource = MessagingStats("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(), ["a", "b", "c"])

                self.resource.list(
                    by="off",
                    start="start",
                    end="end",
                )
                mock_request.assert_called_with("GET", self.resource.uri, params={
                    "by": "off",
                    "start": "start",
                    "end": "end",
                })

                calls = [call("a"), call("b"), call("c")]
                mock_load.assert_has_calls(calls)
                assert mock_load.call_count == 3


class TestSpendingStat(unittest.TestCase):

    def setUp(self):
        self.resource = SpendingStats("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=2,
                start="start",
                end="end"
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 2,
                "start": "start",
                "end": "end",
                "search": False,
            })


class TestInvoices(unittest.TestCase):

    def setUp(self):
        self.resource = Invoices("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                page=3,
                limit=100,
            )
            mock.assert_called_with({
                "limit": 100,
                "page": 3,
                "search": False
            })


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.resource = Utils("uri", ("username", "token"))

    def test_ping(self):
        with patch.object(self.resource, "request") as mock:
            mock.return_value = (Mock(), "data")
            result = self.resource.ping()
            mock.assert_called_with("GET", "%s/%s" % (self.resource.base_uri, "ping"))
            assert result == "data"