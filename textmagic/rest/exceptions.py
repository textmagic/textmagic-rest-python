# -*- coding: utf-8 -*-
import sys
import pprint

from six import u

from ..exceptions import TextmagicException


class TextmagicRestException(TextmagicException):
    """ A generic 400 or 500 level exception from the Textmagic APIv2

    :param int status: HTTP status code that was returned for the exception
    :param str uri:    URI that caused the exception
    :param str msg:    A human-readable message for the error
    :param str method: The HTTP method used to make the request
    """

    def __init__(self, status, uri, msg="", method='GET', errors=None):
        self.uri = uri
        self.status = status
        self.msg = msg
        self.method = method
        self.errors = errors

    def __str__(self):
        """ Try to pretty-print the exception, if this is going on screen. """

        def red(words):
            return u("\033[31m\033[49m%s\033[0m") % words

        def white(words):
            return u("\033[37m\033[49m%s\033[0m") % words

        def blue(words):
            return u("\033[34m\033[49m%s\033[0m") % words

        def teal(words):
            return u("\033[36m\033[49m%s\033[0m") % words

        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            msg = (
                "\n{red_error}\n{request_was}\n\n{http_line}"
                "\n\n{message}\n".format(
                    red_error=red("HTTP Error %s" % self.status),
                    request_was=white("Your request was:"),
                    http_line=teal("%s %s" % (self.method, self.uri)),
                    message=blue(str(self.msg))
                ))
            if self.errors:
                try:
                    msg = "".join([msg, "\n{0}\n".format(
                        white(str(self.errors))
                    )])
                except TypeError:
                    return msg
            return msg
        else:
            pprint.pprint(self.errors)
            return "HTTP {0} error: {1}".format(self.status, self.msg)

