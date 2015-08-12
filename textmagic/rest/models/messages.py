from . import Model, CollectionModel


class Message(Model):
    """
    A Message object model.

    .. attribute:: id

    .. attribute:: receiver

    .. attribute:: messageTime

    .. attribute:: status

    .. attribute:: text

    .. attribute:: charset

    .. attribute:: firstName

    .. attribute:: lastName

    .. attribute:: country

    .. attribute:: sender

    .. attribute:: price

    .. attribute:: partsCount
    """


class Messages(CollectionModel):
    name = "messages"
    form = "msg"
    instance = Message

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`Message` objects and a pager dict.

        :Example:

        messages, pager = client.messages.list()

        :param bool search:     If True then search messages using `ids`, `sessionId`, and/or `query`. Default=False
        :param int  page:       Fetch specified results page. Default=1
        :param int  limit:      How many results on page. Default=10
        :param str  ids:        Find message by ID(s). Using with `search`=True.
        :param str  sessionId:  Find messages by session ID. Using with `search`=True.
        :param str  query:      Find messages by specified search query. Using with `search`=True.
        """
        kwargs["search"] = search
        return self.get_instances(kwargs)

    def create(self, from_=None, **kwargs):
        """
        Create and send a new outbound message.
        Returns :class:`Message` object contains next attributes: 'id', 'href', 'type',
        'sessionId', 'bulkId', 'messageId', 'scheduledId'.

        :Example:

        message = client.messages.create(from_="447624800500", phones="999000001", text="Hello!", lists="1909100")

        :param str text:         Message text. Required if template_id is not set.
        :param str templateId:   Template used instead of message text. Required if text is not set.
        :param str sendingTime:  Message sending time in unix timestamp format. Default is now.
                                 Optional (required with recurrency_rule set).
        :param str contacts:     Contacts ids, separated by comma, message will be sent to.
        :param str lists:        Lists ids, separated by comma, message will be sent to.
        :param str phones:       Phone numbers, separated by comma, message will be sent to.
        :param int cutExtra:     Should sending method cut extra characters
                                 which not fit supplied parts_count or return 400 Bad request response instead.
                                 Default is false.
        :param int partsCount:   Maximum message parts count (TextMagic allows sending 1 to 6 message parts).
                                 Default is 6.
        :param str referenceId:  Custom message reference id which can be used in your application infrastructure.
        :param str from_:        One of allowed Sender ID (phone number or alphanumeric sender ID).
        :param str rrule:        iCal RRULE parameter to create recurrent scheduled messages.
                                 When used, sending_time is mandatory as start point of sending.
        :param int dummy:        If 1, just return message pricing. Message will not send.
        """

        if "dummy" in kwargs and kwargs["dummy"]:
            response, instance = self.request("POST", self.uri, data=kwargs)
            return instance
        if from_:
            kwargs["from"] = from_
        return self.create_instance(kwargs)

    def price(self, from_=None, **kwargs):
        """
        Check pricing for a new outbound message.
        An useful synonym for "message" command with "dummy" parameters set to true.

        :Example:

        message = client.messages.price(from_="447624800500", phones="999000001", text="Hello!", lists="1909100")

        :param str from:         One of allowed Sender ID (phone number or alphanumeric sender ID).
        :param str text:         Message text. Required if template_id is not set.
        :param str templateId:   Template used instead of message text. Required if text is not set.
        :param str sendingTime:  Message sending time in unix timestamp format. Default is now.
                                 Optional (required with recurrency_rule set).
        :param str contacts:     Contacts ids, separated by comma, message will be sent to.
        :param str lists:        Lists ids, separated by comma, message will be sent to.
        :param str phones:       Phone numbers, separated by comma, message will be sent to.
        :param int cutExtra:     Should sending method cut extra characters
                                 which not fit supplied parts_count or return 400 Bad request response instead.
                                 Default is false.
        :param int partsCount:   Maximum message parts count (TextMagic allows sending 1 to 6 message parts).
                                 Default is 6.
        :param str referenceId:  Custom message reference id which can be used in your application infrastructure.
        :param str rrule:        iCal RRULE parameter to create recurrent scheduled messages.
                                 When used, sending_time is mandatory as start point of sending.
        :param int dummy:        If 1, just return message pricing. Message will not send.
        """
        if from_:
            kwargs["from"] = from_
        uri = "%s/%s" % (self.uri, "price")
        response, instance = self.request("GET", uri, params=kwargs)
        return instance

    def delete(self, uid):
        """
        Delete the specified Message from TextMagic.
        Returns True if success.

        :Example:

        client.messages.delete(1901001)

        :param int uid: The unique id of the Message. Required.
        """
        return self.delete_instance(uid)