
try:
    # python 3
    from urllib.parse import urlencode, urlparse, urljoin, urlunparse
except ImportError:
    # python 2
    from urllib import urlencode
    from urlparse import urlparse, urljoin, urlunparse

try:
    # python 2
    from itertools import izip
except ImportError:
    izip = zip

# json
try:
    #python > 2.5
    import json
except ImportError:
    try:
        #python < 2.6
        import simplejson as json
    except ImportError:
        #django
        from django.utils import simplejson as json