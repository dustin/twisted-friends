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

print "Starting feed for", sys.argv[1]

def gotMessage(msg):
    print "Got a message: ", msg.title
    for comment in msg.comments:
        print " + %s" % comment.body

rlp = twistedfriends.RealtimeLongPoll(sys.argv[1], sys.argv[2], gotMessage)

loop = task.LoopingCall(rlp)
loop.start(0, True)

reactor.run()
