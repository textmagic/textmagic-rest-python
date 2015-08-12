from . import Model, CollectionModel


class User(Model):
    """
    An User object model

    .. attribute:: id

    .. attribute:: username

    .. attribute:: firstName

    .. attribute:: lastName

    .. attribute:: balance

    .. attribute:: company

    .. attribute:: currency

        Dictionary like this:
        ::
            {
                "id": "GBP",
                "htmlSymbol": "&pound;"
            }

    .. attribute:: timezone

        Dictionary like this:
        ::
            {
                "area": "Pacific",
                "dst": "0",
                "offset": "-39600",
                "timezone": "Pacific/Midway"
            }

    .. attribute:: subaccountType
    """


class Users(CollectionModel):
    name = "user"
    instance = User
    form = "user"

    def get(self):
        """
        Get current user info.
        Returns :class:`User` object.

        :Example:

        user = client.user.get()
        """
        response, instance = self.request("GET", self.uri)
        return self.load_instance(instance)

    def update(self, **kwargs):
        """
        Update an current User via a PUT request.
        Returns True if success.

        :Example:

        client.user.update(firstName="John", lastName="Doe", company="TextMagic", timezone=1)

        :param str firstName: User first name. Required.
        :param str lastName:  User last name. Required.
        :param str company:   User company. Required.
        """
        response, instance = self.request("PUT", self.uri, data=kwargs)
        return response.status == 201


class Subaccounts(CollectionModel):
    name = "subaccounts"
    instance = User
    searchable = False

    def list(self, **kwargs):
        """
        Returns a list of :class:`User` objects and a pager dict.

        :Example:

        subs, pager = client.subaccounts.list()

        :param int  page:       Fetch specified results page. Default=1
        :param int  limit:      How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def send_invite(self, **kwargs):
        """
        Invite new subaccount.
        Returns True if success.

        :Example:

        s = client.subaccounts.create(email="johndoe@yahoo.com", role="A")

        :param str email: Subaccount email. Required.
        :param str role:  Subaccount role: `A` for administrator or `U` for regular user. Required.
        """
        resp, _ = self.request("POST", self.uri, data=kwargs)
        return resp.status == 204

    def close(self, uid):
        """
        Close subaccount.
        Returns True if success.

        :Example:

        client.subaccounts.close(1901010)

        :param int uid: The unique id of the Subaccount to close.
        """
        return self.delete_instance(uid)


class Invoice(Model):
    """
    An Invoice object model

    .. attribute:: id

    .. attribute:: bundle

    .. attribute:: currency

    .. attribute:: vat

    .. attribute:: paymentMethod
    """


class Invoices(CollectionModel):
    name = "invoices"
    instance = Invoice
    searchable = False

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`Invoice` objects and a pager dict.

        :Example:

        invoices, pager = client.invoices.list()

        :param int  page:       Fetch specified results page. Default=1
        :param int  limit:      How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)