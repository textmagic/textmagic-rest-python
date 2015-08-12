from . import Model, CollectionModel


class Reply(Model):
    """
    A Reply object model (Inbox message)

    .. attribute:: id

    .. attribute:: sender

    .. attribute:: messageTime

    .. attribute:: text

    .. attribute:: receiver
    """


class Replies(CollectionModel):
    name = "replies"
    instance = Reply

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`Reply` objects and a pager dict.

        :Example:

        replies, pager = client.replies.list()

        :param bool search: If True then search replies using `ids` and/or `query`. Default=False
        :param int  page:   Fetch specified results page. Default=1
        :param int  limit:  How many results on page. Default=10
        :param str  ids:    Find replies by ID(s). Using with `search`=True
        :param str  query:  Find replies by specified search query. Using with `search`=True
        """
        kwargs["search"] = search
        return self.get_instances(kwargs)

    def delete(self, uid):
        """
        Delete the specified Reply from TextMagic.
        Returns True if success.

        :Example:

        client.replies.delete(1901001)

        :param int uid: The unique id of the Reply. Required.
        """
        return self.delete_instance(uid)