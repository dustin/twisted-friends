import time
import base64

from twisted.python import log
from twisted.internet import reactor
from twisted.web import client

import ffxml

URL_BASE="http://chan.friendfeed.com/api/updates/home?format=xml&token="

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

def makeAuthHeader(username, authkey):
    headers = {}
    authorization = base64.encodestring('%s:%s' % (username, authkey))[:-1]
    headers['Authorization'] = "Basic %s" % authorization
    return headers

class RealtimeLongPoll(object):

    def __init__(self, username, authkey, msg_handler):
        self.ff_token = ""
        self.last_update = None
        self.username = username
        self.authkey = authkey
        self.msg_handler = msg_handler

    def __call__(self):
        log.msg("RealtimeLongPoll iterating")

        # Convert this from unicode
        url = str(URL_BASE + self.ff_token)
        
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