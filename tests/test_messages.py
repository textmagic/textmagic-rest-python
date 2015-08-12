import unittest
from mock import patch, Mock
from textmagic.rest.models import Bulks, Messages, Chats, Replies, Schedules, Sessions


class TestChat(unittest.TestCase):

    def setUp(self):
        self.resource = Chats("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(page=1, limit=25)
            mock.assert_called_with({
                "page": 1,
                "limit": 25,
                "search": False
            })


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.resource = Messages("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=50,
                page=3
            )
            mock.assert_called_with({
                "limit": 50,
                "page": 3,
                "search": False,
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=3,
                search=True,
                sessionId=123
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 3,
                "search": True,
                "sessionId": 123
            })

    def test_create(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(
                text="mock text",
                contacts="888, 999",
                sendingTime=12345
            )
            mock.assert_called_with({
                "text": "mock text",
                "contacts": "888, 999",
                "sendingTime": 12345
            })

    def test_create_from(self):
        with patch.object(self.resource, "create_instance") as mock:
            self.resource.create(
                text="mock",
                phones="999123, 999999",
                from_="SENDER_ID",
            )
            mock.assert_called_with({
                "text": "mock",
                "phones": "999123, 999999",
                "from": "SENDER_ID",
            })

    def test_create_dummy(self):
        with patch.object(self.resource, "request") as mock:
            json_price = '{"total":1, "price":0}'
            mock.return_value = (Mock(), json_price)

            result = self.resource.create(
                text="mock",
                phones="999999",
                dummy=1
            )

            mock.assert_called_with(
                "POST",
                self.resource.uri,
                data={
                    "text": "mock",
                    "dummy": 1,
                    "phones": "999999",
                }
            )
            assert result == json_price

    def test_price(self):
        with patch.object(self.resource, "request") as mock:
            json_price = '{"total":1, "price":0}'
            mock.return_value = (Mock(), json_price)

            result = self.resource.price(
                text="mock",
                phones="999999",
                from_="5550000"
            )

            mock.assert_called_with(
                "GET",
                "%s/%s" % (self.resource.uri, "price"),
                params={
                    "text": "mock",
                    "from": "5550000",
                    "phones": "999999",
                }
            )
            assert result == json_price

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(999)
            mock.assert_called_with(999)


class TestReply(unittest.TestCase):

    def setUp(self):
        self.resource = Replies("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=25,
                page=2,
            )
            mock.assert_called_with({
                "limit": 25,
                "page": 2,
                "search": False
            })

    def test_list_search(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                limit=10,
                page=5,
                search=True,
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 5,
                "search": True
            })

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(123)
            mock.assert_called_with(123)


class TestSchedule(unittest.TestCase):

    def setUp(self):
        self.resource = Schedules("uri", ("username", "token"))

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
            )
            mock.assert_called_with({
                "limit": 10,
                "page": 1,
                "search": False,
            })

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(123)
            mock.assert_called_with(123)


class TestSession(unittest.TestCase):

    def setUp(self):
        self.resource = Sessions("uri", ("username", "token"))

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

    def test_delete(self):
        with patch.object(self.resource, "delete_instance") as mock:
            self.resource.delete(9090)
            mock.assert_called_with(9090)


class TestBulk(unittest.TestCase):

    def setUp(self):
        self.resource = Bulks("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, "get_instances") as mock:
            self.resource.list(
                page=2,
                limit=10,
            )
            mock.assert_called_with({
                "page": 2,
                "limit": 10,
                "search": False
            })