from . import Model, CollectionModel, Messages


class Session(Model):
    """
    A Session object model

    .. attribute:: id

    .. attribute:: startTime

    .. attribute:: text

    .. attribute:: source

    .. attribute:: referenceId

    .. attribute:: price

    .. attribute:: numbersCount
    """


class Sessions(CollectionModel):
    name = "sessions"
    searchable = False
    instance = Session

    def list(self, **kwargs):
        """
        Returns a list of :class:`Session` objects and a pager dict.

        :Example:

        sessions, pager = client.sessions.list()

        :param int  page:     Fetch specified results page. Default=1
        :param int  limit:    How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def delete(self, uid):
        """
        Delete the specified Session from Textmagic.
        Returns True if success.

        :Example:

        client.sessions.delete(1901001)

        :param int uid: The unique id of the Session. Required.
        """
        return self.delete_instance(uid)

    def messages(self, uid=0, **kwargs):
        """
        Fetch messages by given session id.
        An useful synonym for "messages/search" command with provided `sessionId` parameter.
        Returns a list of :class:`Message` objects and a pager dict.

        :Example:

        messages = client.sessions.messages(1901001)

        :param int uid:   The unique id of the Session. Required.
        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        messages = Messages(self.base_uri, self.auth)
        return self.get_subresource_instances(uid, instance=messages,
                                              resource="messages", params=kwargs)