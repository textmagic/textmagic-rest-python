from . import Model, CollectionModel


class Stat(Model):
    """
    A Stat object model
    """


class MessagingStat(Stat):
    """
    MessagingStat object model

    .. attribute:: replyRate

    .. attribute:: date

    .. attribute:: deliveryRate

    .. attribute:: costs

    .. attribute:: messagesReceived

    .. attribute:: messagesSentDelivered

    .. attribute:: messagesSentAccepted

    .. attribute:: messagesSentBuffered

    .. attribute:: messagesSentFailed

    .. attribute:: messagesSentRejected

    .. attribute:: messagesSentParts
    """


class SpendingStat(Stat):
    """
    SpendingStat object model

    .. attribute:: id

    .. attribute:: userId

    .. attribute:: date

    .. attribute:: balance

    .. attribute:: delta

    .. attribute:: type

    .. attribute:: value

    .. attribute:: comment
    """


class MessagingStats(CollectionModel):
    name = "stats/messaging"
    instance = MessagingStat

    def list(self, **kwargs):
        """
        Returns a list of :class:`MessagingStat` objects (messaging statistics).

        :Example:

        stats = client.stats_messaging.list()

        :param str by:    Group results by specified period: `off`, `day`, `month` or `year`. Default is `off`.
        :param str start: Start date in unix timestamp format. Default is 7 days ago.
        :param str end:   End date in unix timestamp format. Default is now.
        """
        response, instances = self.request("GET", self.uri, params=kwargs)
        return [self.load_instance(r) for r in instances]


class SpendingStats(CollectionModel):
    name = "stats/spending"
    instance = SpendingStat

    def list(self, **kwargs):
        """
        Returns a list of :class:`SpendingStat` objects (account spending statistics) and a pager dict.

        :Example:

        stats, pager = client.stats_spending.list()

        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        :param str start: Start date in unix timestamp format. Default is 7 days ago.
        :param str end:   End date in unix timestamp format. Default is now.
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

