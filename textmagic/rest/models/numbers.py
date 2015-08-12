from . import Model, CollectionModel


class Number(Model):
    """
    A Number object model

    .. attribute:: id

    .. attribute:: user

        Dictionary like this:
        ::
            {
                "id": 62931,
                "username": "johndoe",
                "firstName": "John",
                "lastName": "Doe",
                "status": "A",
                "balance": 13.793,
                "company": "TextMagic",
                "currency": {
                    "id": "GBP",
                    "htmlSymbol": "&pound;"
                },
                "timezone": {
                    "id": 2,
                    "area": "Pacific",
                    "dst": 0,
                    "offset": -39600,
                    "timezone": "Pacific/Midway"
                },
                "subaccountType": "P"
            }

    .. attribute:: purchasedAt

    .. attribute:: expireAt

    .. attribute:: phone

    .. attribute:: country

        Dictionary like this:
        ::
            {
                "id": "US",
                "name": "United States"
            }

    .. attribute:: status
    """


class Numbers(CollectionModel):
    name = "numbers"
    instance = Number
    searchable = False

    def list(self, **kwargs):
        """
        Returns a list of :class:`Number` objects and a pager dict.

        :Example:

        numbers, pager = client.numbers.list()

        :param int  page:     Fetch specified results page. Default=1
        :param int  limit:    How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def buy(self, **kwargs):
        """
        Buy a dedicated number and assign it to the specified account.
        Returns :class:`Number` object contains id and link to Number.

        :Example:

        number = client.numbers.create(phone="16463501784", country="US", userId="111")

        :param str phone:   Desired dedicated phone number in international E.164 format. Required.
        :param str country: Dedicated number country. Required.
        :param str userId:  User ID this number will be assigned to. Required.
        """

        return self.create_instance(kwargs)

    def available(self, **kwargs):
        """
        Find available dedicated numbers to buy. Returns dictionary like this:
        ::
            {
                "numbers": [
                "12146124143",
                "12172100315",
                "12172100317",
                "12172100319",
                "12172100321",
                "12172100323",
                "12172100325",
                "12172100326",
                "12172100327",
                "12172100328"
              ],
              "price": 2.4
            }

        :Example:

        numbers = client.numbers.available(country="US")

        :param str country: Dedicated number country. Required.
        :param str prefix:  Desired number prefix. Should include country code (i.e. 447 for GB)
        """
        uri = "%s/%s" % (self.uri, "available")
        response, instance = self.request("GET", uri, params=kwargs)
        return instance

    def delete(self, uid):
        """
        Cancel dedicated number subscription.
        Returns True if success.

        :Example:

        client.numbers.delete(1901001)

        :param int uid: The unique id of the Number. Required.
        """
        return self.delete_instance(uid)


class Senderid(Model):
    """
    A Sender ID object model

    .. attribute:: id

    .. attribute:: senderId

    .. attribute:: user

        Dictionary like this:
        ::
            {
                "id": 11111,
                "username": "johndoe",
                "firstName": "John",
                "lastName": "Doe",
                "status": "A",
                "balance": 13.793,
                "company": "TextMagic",
                "currency": {
                    "id": "GBP",
                    "htmlSymbol": "&pound;"
                },
                "timezone": {
                    "id": 2,
                    "area": "Pacific",
                    "dst": 0,
                    "offset": -39600,
                    "timezone": "Pacific/Midway"
                },
                "subaccountType": "P"
            }

    .. attribute:: status
    """


class Senderids(CollectionModel):
    name = "senderids"
    instance = Senderid
    searchable = False

    def list(self, **kwargs):
        """
        Returns a list of :class:`Senderid` objects and a pager dict.

        :Example:

        senderids, pager = client.senderids.list()

        :param int  page:     Fetch specified results page. Default=1
        :param int  limit:    How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Create a new senderid.
        Returns :class:`Senderid` object contains id and link to Senderid.

        :Example:

        senderid = client.senderids.create(senderId="TEST", explanation="For testing")

        :param str senderId:    Alphanumeric Sender ID (maximum 11 characters). Required.
        :param str explanation: Explain why do you need this Sender ID. Required.
        """
        return self.create_instance(kwargs)

    def delete(self, uid):
        """
        Delete the specified Sender ID from TextMagic.
        Returns True if success.

        :Example:

        client.senderids.delete(1901010)

        :param int uid: The unique id of the Sender ID to delete (numeric, not alphanumeric Sender ID itself). Required.
        """
        return self.delete_instance(uid)


class Source(Model):
    """
    A Source object model. Contains allowed sender ids, shared and dedicated numbers.

    .. attribute:: dedicated

    .. attribute:: shared

    .. attribute:: senderIds
    """


class Sources(CollectionModel):
    name = "sources"
    instance = Source
    searchable = False

    def allowed(self, **kwargs):
        """
        Get all available sender settings which could be used in "from" parameter of POST messages method.
        Returns :class:`Source` object.

        :Example:

        allowed = client.sources.allowed()

        :param country:  Return sender settings available in specified country only. Optional.
        """
        resp, instance = self.request("GET", self.uri, params=kwargs)
        return self.load_instance(instance)