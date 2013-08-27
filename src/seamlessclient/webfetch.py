from seamlessclient.config import Config
from urllib2 import URLError, HTTPError
import urllib2
import simplejson
class NotFound(BaseException):
    pass

def make_correct_host(host):
    url = host
    if not url.startswith("http://"):
        url = "http://" + url
    if not url.endswith("/"):
        url = url + "/"
    return url


def make_url(host, function, parameter):
    if parameter is not None:
        return make_correct_host(host) + "api/" + function + "/" + parameter + "/"
    else:
        return make_correct_host(host) + "api/" + function + "/"


def make_user_url(host, uuid):
    return make_correct_host(host) + "show/" + uuid + "/"


def get_by_uniquename(uniquename):
    return run_server_request("get-by-uniquename", uniquename)
    
def run_server_request(function, parameter = None):
    try:
        url = make_url(Config().get_server(), function, parameter)
        response = urllib2.urlopen(url)
        json = response.read()
        return simplejson.loads(json, encoding="UTF-8")
    except HTTPError as e:
        #print 'The server couldn\'t fulfill the request.'
        #print 'Error code: ', e.code
        raise NotFound()
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        raise NotFound()
    except:
        print 'Something failed'
        raise NotFound()