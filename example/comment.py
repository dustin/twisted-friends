#!/usr/bin/env python
"""

Copyright (c) 2008  Dustin Sallings <dustin@spy.net>
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))
sys.path.append('lib')

from twisted.internet import reactor
from twisted.python import log

log.startLogging(sys.stdout)

import twistedfriends

def yes(x): print "Posted:", x
def no(x): print "Failed to post: ", x

d = twistedfriends.add_comment(sys.argv[1], sys.argv[2],
    sys.argv[3], sys.argv[4])
d.addCallback(yes)
d.addErrback(no)
d.addBoth(lambda x: reactor.stop())

reactor.run()
