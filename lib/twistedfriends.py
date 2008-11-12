import time
import base64
import urllib

from twisted.python import log
from twisted.internet import reactor
from twisted.web import client

import ffxml

URL_BASE="http://chan.friendfeed.com/api/updates"

class DownloadWithHeadersFactory(client.HTTPDownloader):

    def __init__(self, url, fileOrName, headerCallback,
                 method='GET', postdata=None, headers=None,
                 agent="Twisted client", supportPartial=0):
        client.HTTPDownloader.__init__(self, url, fileOrName,
                method, postdata, headers, agent, supportPartial)
        self.headerCallback = headerCallback

    def gotHeaders(self, headers):
        client.HTTPDownloader.gotHeaders(self, headers)
        self.headerCallback.gotHeaders(headers)

def getPageWithHeaders(url, file, headerCallback, contextFactory=None,
        *args, **kwargs):
    scheme, host, port, path = client._parse(url)
    factory = DownloadWithHeadersFactory(url, file, headerCallback,
        *args, **kwargs)
    if scheme == 'https':
        from twisted.internet import ssl
        if contextFactory is None:
            contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(host, port, factory, contextFactory)
    else:
        reactor.connectTCP(host, port, factory)
    return factory.deferred

def makeAuthHeader(username, authkey, headers=None):
    if not headers:
        headers = {}
    authorization = base64.encodestring('%s:%s' % (username, authkey))[:-1]
    headers['Authorization'] = "Basic %s" % authorization
    return headers

class RealtimeLongPoll(object):

    def __init__(self, username, authkey, msg_handler, path="/home"):
        self.ff_token = None
        self.username = username
        self.authkey = authkey
        self.msg_handler = msg_handler
        self.path = path

    def __call__(self):
        log.msg("RealtimeLongPoll iterating")

        # Convert this from unicode
        if self.ff_token:
            url = str(URL_BASE + self.path + "?format=xml&token="
                + self.ff_token)
        else:
            url = URL_BASE + "?format=xml"

        return getPageWithHeaders(url, ffxml.Feed(self), self,
            headers=makeAuthHeader(self.username, self.authkey)
            ).addErrback(self.onError)

    def gotHeaders(self, headers):
        self.serverDate = self._parseDate(headers['date'][0])

    def _parseDate(self, d):
        return time.strptime(d, '%a, %d %b %Y %H:%M:%S GMT')

    def gotUpdate(self, token, poll_interval, incomplete):
        self.ff_token = token

    def gotEntry(self, e):
        self.msg_handler(e)

    def onError(self, err):
        raise err

def validateCredentials(username, authkey):
    return client.getPage("http://friendfeed.com/api/validate",
        headers=makeAuthHeader(username, authkey))

def __urlencode(h):
    rv = []
    for k,v in h.iteritems():
        rv.append('%s=%s' %
            (urllib.quote(k.encode("utf-8")), urllib.quote(v.encode("utf-8"))))
    return '&'.join(rv)

def __post(user, remotekey, path, args):
    h = {'Content-Type': 'application/x-www-form-urlencoded'}
    return client.getPage("http://friendfeed.com%s" % path, method='POST',
        postdata=__urlencode(args),
        headers=makeAuthHeader(user, remotekey, h))

def publish_message(user, remotekey, message, via=None):
    args = {'title': message}
    if via: args['via'] = via
    return __post(user, remotekey, '/api/share', args)

def add_comment(user, remotekey, entry_id, body, via=None):
    args = {'entry': entry_id, 'body': body}
    if via: args['via'] = via
    return __post(user, remotekey, '/api/comment', args)

def like(user, remotekey, entry_id):
    return __post(user, remotekey, '/api/like', {'entry': entry_id})
