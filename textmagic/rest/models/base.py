import platform
import httplib2
import os


from six import (
    iteritems,
    string_types,
    integer_types,
    binary_type,
)
from ...compat import json, urlencode, urlparse
from ...version import __version__
from ..exceptions import TextmagicRestException


class Response(object):
    def __init__(self, httplib_response, content, url):
        self.content = content
        self.status = int(httplib_response.status)
        self.ok = self.status < 400
        self.url = url


def get_cert_file():
    """ Get the certificates file for https"""
    try:
        current_path = os.path.realpath(__file__)
        ca_cert_path = os.path.join(current_path, "..", "..", "..",
                                    "conf", "cacert.pem")
        return os.path.abspath(ca_cert_path)
    except Exception:
        return None


def make_request(method, url, params=None, data=None, headers=None, auth=None):
    """
    Make an HTTP request.

    :param str   method:  "POST", "GET", "PUT" or "DELETE"
    :param str   url:     URL to process request.
    :param dict  params:  Params to add to the URL.
    :param dict  data:    Form data.
    :param dict  headers: Headers to request.
    :param tuple auth:    Username and token.
    """

    http = httplib2.Http(
        ca_certs=get_cert_file(),
    )

    if auth is not None:
        http.add_credentials(auth[0], auth[1])

    if params is not None:
        enc_params = urlencode(params, doseq=True)
        if urlparse(url).query:
            url = '%s&%s' % (url, enc_params)
        else:
            url = '%s?%s' % (url, enc_params)
        params["_format"] = "json"

    def encode_atom(atom):
        if isinstance(atom, (integer_types, binary_type)):
            return atom
        elif isinstance(atom, string_types):
            return atom.encode('utf-8')
        else:
            raise ValueError('list elements should be an integer, '
                             'binary, or string')

    if data is not None:
        udata = {}
        for k, v in iteritems(data):
            key = k.encode('utf-8')
            if isinstance(v, (list, tuple, set)):
                udata[key] = [encode_atom(x) for x in v]
            elif isinstance(v, (integer_types, binary_type, string_types)):
                udata[key] = encode_atom(v)
            else:
                raise ValueError('data should be an integer, '
                                 'binary, or string, or sequence ')
        data = udata
        data = urlencode(udata, doseq=True)

    response, content = http.request(uri=url, method=method,
                                     headers=headers, body=data)

    return Response(response, content, url)


def make_tm_request(method, uri, **kwargs):
    """
    Make a request to TextMagic REST APIv2.

    :param str method: "POST", "GET", "PUT" or "DELETE"
    :param str uri:    URI to process request.
    :return: :class:`Response`
    """
    headers = kwargs.get("headers", {})

    user_agent = "textmagic-python/%s (Python %s)" % (
        __version__,
        platform.python_version()
    )
    headers["User-agent"] = user_agent
    headers["Accept-Charset"] = "utf-8"
    if "Accept-Language" not in headers:
        headers["Accept-Language"] = "en-us"

    if (method == "POST" or method == "PUT") and "Content-Type" not in headers:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    kwargs["headers"] = headers

    if "Accept" not in headers:
        headers["Accept"] = "application/json"

    headers["X-TM-Username"], headers["X-TM-Key"] = kwargs["auth"]

    response = make_request(method, uri, **kwargs)

    if not response.ok:
        try:
            resp_body = json.loads(response.content)
            message = resp_body["message"]
            errors = resp_body["errors"]
        except:
            message = response.content
            errors = None

        raise TextmagicRestException(status=response.status, method=method, uri=response.url,
                                     msg=message, errors=errors)

    return response


class Model(object):
    """
    REST APIv2 base model class.
    """

    def __init__(self, base, auth):
        self.base_uri = base
        self.auth = auth

    def request(self, method, uri, **kwargs):
        """
        Send an HTTP request.

        :param str method: "POST", "GET", "PUT" or "DELETE"
        :param str uri:    URI to process request.
        :raises :class:`TextmagicRestException`
        """

        response = make_tm_request(method, uri, auth=self.auth, **kwargs)

        if method == "DELETE" or response.status == 204:
            return response, {}
        else:
            return response, json.loads(response.content.decode("utf-8"))

    def load(self, entries):
        del self.base_uri
        del self.auth
        self.__dict__.update(entries)

    @property
    def uri(self):
        return "%s/%s" % (self.base_uri, self.name)


class CollectionModel(Model):
    name = "model"
    form = None
    instance = Model
    searchable = True

    def __init__(self, *args, **kwargs):
        super(CollectionModel, self).__init__(*args, **kwargs)

    def get(self, uid):
        return self.get_instance(uid)

    def get_instance(self, uid):
        uri = "%s/%s" % (self.uri, uid)
        response, instance = self.request("GET", uri)
        return self.load_instance(instance)

    def get_instances(self, params):
        uri = self.uri
        if "search" in params and params["search"]:
            uri += "/search"
        response, page = self.request("GET", uri, params=params)
        resources = page.pop("resources", [])
        return [self.load_instance(r) for r in resources], page

    def get_subresource_instances(self, uid=0, instance=None, resource=None, params={}):
        uri = "%s/%s" % (self.uri, uid)
        if resource:
            uri += "/%s" % resource
        if not instance:
            instance = self
        response, page = self.request("GET", uri, params=params)
        resources = page.pop("resources", [])
        return [instance.load_instance(r) for r in resources], page

    def load_instance(self, data):
        instance = self.instance(self.base_uri, self.auth)
        instance.load(data)
        return instance

    def create_instance(self, data):
        response, instance = self.request("POST", self.uri, data=data)

        if response.status not in (200, 201):
            raise TextmagicRestException(response.status, self.uri, "Resource not created")

        return self.load_instance(instance)

    def update_instance(self, uid, body):
        """
        Update an Model via a PUT request

        :param str  uid:  String identifier for the list resource
        :param dict body: Dictionary of items to PUT
        """
        uri = "%s/%s" % (self.uri, uid)
        response, instance = self.request("PUT", uri, data=body)
        return self.load_instance(instance)

    def update_subresource_instance(self, uid, body, subresource=None, slug=None):
        uri = "%s/%s" % (self.uri, uid)
        if slug:
            uri += "/%s" % slug
        if not subresource:
            subresource = self
        response, instance = self.request("PUT", uri, data=body)
        return subresource.load_instance(instance)

    def delete_instance(self, uid):
        """
        Delete an ObjectModel via a DELETE request

        :param int uid: Unique id for the Model resource
        """
        uri = "%s/%s" % (self.uri, uid)
        response, instance = self.request("DELETE", uri)
        return response.status == 204