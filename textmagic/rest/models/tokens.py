from . import Model, CollectionModel


class Token(Model):
    """
    A Token object model

    .. attribute:: username

    .. attribute:: token

    .. attribute:: expires
    """


class Tokens(CollectionModel):
    name = "tokens"
    instance = Token

    def create(self, username, password):
        """
        Create Token by given username and password.
        Authenticate user by given username and password.
        Returning a :class:`Token` object contains username and token that you should pass to the all requests
        (in X-TM-Username and X-TM-Key, respectively).

        :Example:

        token = client.tokens.create(username="my_username", password="my_password")

        :param username: Account username or email. Required.
        :param password: Account password. Required.
        """
        data = dict(username=username, password=password)
        response, instance = self.request("POST", self.uri, data=data)
        return self.load_instance(instance)

    def refresh(self):
        """
        Refresh access token. Only non-expired tokens can be renewed.

        :Example:

        token = client.tokens.refresh()
        """
        uri = "%s/%s" % (self.uri, "refresh")
        response, instance = self.request("GET", uri)
        return response.ok