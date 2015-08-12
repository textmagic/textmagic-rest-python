import unittest
from mock import patch, call, Mock
from textmagic.compat import json
from textmagic import TextmagicException
from textmagic.rest.models import CollectionModel, Model

base = "http://api.textmagic.com/api/v2"
username = "username"
token = "token"
auth = (username, token)


class TestCollectionModel(unittest.TestCase):

    def setUp(self):
        self.resource = CollectionModel(base, auth)

    def test_uri_init(self):
        uri = "%s/%s" % (base, self.resource.name)
        assert self.resource.uri == uri

    def test_get(self):
        with patch.object(self.resource, "get_instance") as mock:
            self.resource.get(111)
            mock.assert_called_with(111)

    def test_get_instance(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(), ["instance"])

                self.resource.get_instance(101)

                mock_request.assert_called_with("GET", "%s/%s" % (self.resource.uri, 101))
                mock_load.assert_called_with(["instance"])

    def test_get_instances(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(), {"resources": ["a", "b", "c"]})

                self.resource.get_instances({"foo": "abc"})

                mock_request.assert_called_with("GET", self.resource.uri, params={"foo": "abc"})

                calls = [call("a"), call("b"), call("c")]
                mock_load.assert_has_calls(calls)

                self.resource.get_instances({"search": True, "foo": "abc"})

                mock_request.assert_called_with(
                    "GET",
                    "%s/%s" % (self.resource.uri, "search"),
                    params={"foo": "abc", "search": True}
                )

    def test_get_subresource_instances(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:

                mock_request.return_value = (Mock(), {"resources": ["abc", "def"]})

                self.resource.get_subresource_instances(
                    123,
                    instance=self.resource,
                    params={"abc": "foo"}
                )

                uri = "%s/%s" % (self.resource.uri, 123)
                mock_request.assert_called_with(
                    "GET",
                    uri,
                    params={"abc": "foo"}
                )

                calls = [call("abc"), call("def")]
                mock_load.assert_has_calls(calls)

                self.resource.get_subresource_instances(
                    123,
                    resource="obj",
                    params={"a": "b"}
                )

                uri = "%s/%s/obj" % (self.resource.uri, 123)
                mock_request.assert_called_with(
                    "GET",
                    uri,
                    params={"a": "b"}
                )

    def test_load_instance(self):
        instance = self.resource.load_instance({"foo": "abc"})

        assert isinstance(instance, Model)
        assert instance.foo == "abc"

    def test_create_instance(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(status=201), "{json instance}")
                self.resource.create_instance(data={"foo": "abc"})

                mock_request.assert_called_with(
                    "POST",
                    self.resource.uri,
                    data={"foo": "abc"}
                )
                mock_load.assert_called_with("{json instance}")

                mock_request.return_value = (Mock(status=200), "{json instance}")
                self.resource.create_instance(data={"foo": "abc"})

                mock_request.assert_called_with(
                    "POST",
                    self.resource.uri,
                    data={"foo": "abc"}
                )
                mock_load.assert_called_with("{json instance}")

                mock_request.return_value = (Mock(status=404), "{json instance}")

                self.assertRaises(TextmagicException, self.resource.create_instance, {"foo": "abc"})

                mock_request.assert_called_with(
                    "POST",
                    self.resource.uri,
                    data={"foo": "abc"}
                )

    def test_update_instance(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:
                mock_request.return_value = (Mock(), "instance")

                self.resource.update_instance(111, {"foo": "zzz"})

                mock_request.assert_called_with(
                    "PUT",
                    "%s/%s" % (self.resource.uri, 111),
                    data={"foo": "zzz"}
                )

                mock_load.assert_called_once_with("instance")

    def test_update_subresource_instance(self):
        with patch.object(self.resource, "request") as mock_request:
            with patch.object(self.resource, "load_instance") as mock_load:

                mock_request.return_value = (Mock(), "instance")
                self.resource.update_subresource_instance(
                    123,
                    body={"a": "foo"},
                )
                mock_request.assert_called_with(
                    "PUT",
                    "%s/%s" % (self.resource.uri, 123),
                    data={"a": "foo"}
                )
                mock_load.assert_called_with("instance")

                self.resource.update_subresource_instance(
                    123,
                    body={"a": "foo"},
                    slug="abc"
                )
                mock_request.assert_called_with(
                    "PUT",
                    "%s/%s/abc" % (self.resource.uri, 123),
                    data={"a": "foo"}
                )
                mock_load.assert_called_with("instance")

    def test_delete_instance(self):
        with patch.object(self.resource, "request") as mock:
            mock.return_value = (Mock(status=204), "instance")
            r = self.resource.delete_instance(100)
            mock.assert_called_with(
                "DELETE",
                "%s/%s" % (self.resource.uri, 100)
            )

            self.assertTrue(r)


class TestModel(unittest.TestCase):

    def setUp(self):
        self.resource = Model(base, auth)

    def test_init(self):
        assert self.resource.base_uri == base
        assert self.resource.auth == auth

    def test_load(self):
        self.resource.load({
            "abc": "foo",
        })
        assert self.resource.abc == "foo"

    @patch("textmagic.rest.models.base.make_tm_request")
    def test_request(self, mock_tm_request):
        response = Mock(content=b'{"foo": "aaa"}')
        mock_tm_request.return_value = response
        r, content = self.resource.request("GET", base, foo="abc")
        mock_tm_request.assert_called_with(
            "GET",
            base,
            auth=auth,
            foo="abc"
        )

        assert (r, content) == (response, json.loads(b'{"foo": "aaa"}'.decode("utf-8")))

        response = Mock(content=b'{"foo": "aaa"}')
        mock_tm_request.return_value = response
        r, content = self.resource.request("DELETE", base, foo="abc")
        mock_tm_request.assert_called_with(
            "DELETE",
            base,
            auth=auth,
            foo="abc"
        )

        assert (r, content) == (response, {})