from . import Model, CollectionModel


class Schedule(Model):
    """
    A Schedule object model

    .. attribute:: id

    .. attribute:: nextSend

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

    .. attribute:: rrule

    """


class Schedules(CollectionModel):
    name = "schedules"
    instance = Schedule

    def list(self, **kwargs):
        """
        Returns a list of :class:`Schedule` objects and a pager dict.

        :Example:

        schedules, pager = client.schedules.list()

        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def delete(self, uid):
        """
        Delete the specified Schedule from Textmagic.
        Returns True if success.

        :Example:

        client.schedules.delete(1901001)

        :param int uid: The unique id of the Schedule. Required.
        """
        return self.delete_instance(uid)
