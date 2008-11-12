#!/usr/bin/env python
"""

Copyright (c) 2008  Dustin Sallings <dustin@spy.net>
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))
sys.path.append('lib')

from twisted.internet import reactor, protocol, defer, task

import twistedfriends

class CB(object):
    def gotEntry(self, msg):
        print "Got a entry: ", msg.title
        for comment in msg.comments:
            print " + %s" % comment.body

twistedfriends.url_info(sys.argv[1], CB(), *sys.argv[2:]).addBoth(
    lambda x: reactor.stop())

reactor.run()
