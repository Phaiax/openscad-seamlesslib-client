from application.config import Config
from urllib2 import URLError, HTTPError
import urllib2
import simplejson
class NotFound():
    pass

def make_url(host, function, parameter):
    url = host
    if not url.startswith("http://"):
        url = "http://" + url
    if not url.endswith("/"):
        url = url + "/"
    url = url + "api/" + function + "/" + parameter + "/"
    return url

def get_by_uniquename(uniquename):
    try:
        url = make_url(Config().get_server(), "get-by-uniquename", uniquename)
        response = urllib2.urlopen(url)
        json = response.read()
        return simplejson.loads(json, encoding="UTF-8")
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        raise NotFound()
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        raise NotFound()
    except:
        print 'Something failed'
        raise NotFound()
    