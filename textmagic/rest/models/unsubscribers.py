from . import Model, CollectionModel


class Unsubscriber(Model):
    """
    An Unsubsriber object model

    .. attribute:: id

    .. attribute:: phone

    .. attribute:: firstName

    .. attribute:: lastName

    .. attribute:: unsubscribeTime
    """


class Unsubscribers(CollectionModel):
    name = "unsubscribers"
    form = "unsubscriber"
    instance = Unsubscriber

    def list(self, **kwargs):
        """
        Returns a list of :class:`Unsubscriber` objects and a pager dict.

        :Example:

        unsubscribers, pager = client.unsubscribers.list()

        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Unsubscribe contact from your communication by phone number.
        Returns :class:`Unsubscriber` object contains id and link to Unsubscriber.

        :Example:

        client.unsubscribers.create(phone="19025555555")

        :param str phone: Contact phone number you want to unsubscribe. Required.
        """
        return self.create_instance(kwargs)