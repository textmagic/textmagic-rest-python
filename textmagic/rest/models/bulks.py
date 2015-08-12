from . import Model, CollectionModel


class Bulk(Model):
    """
    A bulk object model (Bulk messages session)

    .. attribute:: id

    .. attribute:: status

    .. attribute:: itemsProcessed

    .. attribute:: itemsTotal

    .. attribute:: createdAt

    .. attribute:: text

    .. attribute:: session

        Dictionary like this:
        ::
            {
                "id": "34435949",
                "startTime": "2015-05-01T21:30:00+0000",
                "text": "error",
                "source": "O",
                "referenceId": "O_xxx_cb5e100e5a9a3e7f6d1fd97512215282_10580074905542fc46b9f157.39758261",
                "price": 0.03,
                "numbersCount": 1
            }
    """


class Bulks(CollectionModel):
    name = "bulks"
    searchable = False
    instance = Bulk

    def list(self, **kwargs):
        """
        Returns a list of :class:`Bulk` objects and a pager dict.

        :Example:

        bulks, pager = client.bulks.list()

        :param int  page:  Fetch specified results page. Default=1
        :param int  limit: How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)