from . import Model


class Utils(Model):

    def ping(self):
        """
        Ping.

        :Example:

        ping = client.util.ping()
        """
        uri = "%s/%s" % (self.base_uri, "ping")
        resp, data = self.request("GET", uri)
        return data