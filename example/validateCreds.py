#!/usr/bin/env python
"""

Copyright (c) 2008  Dustin Sallings <dustin@spy.net>
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'lib'))
sys.path.append('lib')

from twisted.internet import reactor

import twistedfriends

def yes(x): print ":) Creds are good!"
def no(x): print ":( Creds are bad!"

d = twistedfriends.validateCredentials(sys.argv[1], sys.argv[2])
d.addCallback(yes)
d.addErrback(no)
d.addBoth(lambda x: reactor.stop())

reactor.run()
