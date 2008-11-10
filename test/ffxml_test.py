#!/usr/bin/env python
"""

Copyright (c) 2008  Dustin Sallings <dustin@spy.net>
"""

import sys
sys.path.append("lib")
sys.path.append("../lib")

import unittest

import ffxml

class XMLParserTest(unittest.TestCase):

    def testParsing(self):
        # This needs to do something useful...
        ts=self
        class D(object):
            def gotUpdate(self, token, poll_interval, incomplete):
                ts.assertEquals('39180875991', token)
                ts.assertEquals('40', poll_interval)
                ts.assertEquals('False', incomplete)
            def gotEntry(self, e):
                ts.assertEquals("2008-11-03T19:43:09Z", e.updated)
                ts.assertEquals("Ken Sheppardson just committed a change to enjit on GitHub",
                    e.title)
                ts.assertEquals("True", e.is_new)
                ts.assertEquals("http://github.com/kshep/enjit/commit/dd3ed5a5421e465e2e2dee8130032eefaff29bb8",
                    e.link)
                ts.assertEquals("False", e.anonymous)
                ts.assertEquals("2008-11-03T19:43:09Z", e.published)
                ts.assertEquals("False", e.hidden)
                ts.assertEquals("0d751d07-a439-49a5-9c26-afda3d1fdea3", e.id)
                # Via
                ts.assertEquals("http://github.com/", e.via.url)
                ts.assertEquals("GitHub", e.via.name)
                # Service
                ts.assertEquals("http://friendfeed.com/", e.service.profileUrl)
                ts.assertEquals("http://chan.friendfeed.com/static/images/icons/internal.png?v=e471e9afdf04ae568dcbddb5584fc6c0",
                    e.service.iconUrl)
                ts.assertEquals("internal", e.service.id)
                ts.assertEquals("link", e.service.entryType)
                ts.assertEquals("FriendFeed", e.service.name)
                # User
                ts.assertEquals("http://chan.friendfeed.com/kshep",
                    e.user.profileUrl)
                ts.assertEquals("kshep", e.user.nickname)
                ts.assertEquals("46958b7d-4bde-4890-8842-8cc33e8f55bd",
                    e.user.id)
                ts.assertEquals("Ken Sheppardson", e.user.name)
                # Comment
                c=e.comments[0]
                ts.assertEquals("dd3ed5a5421e465e2e2dee8130032eefaff29bb8 - Fix for UnicodeEncodeError",
                    c.body)
                ts.assertEquals("True", c.is_new)
                ts.assertEquals("2008-11-03T19:43:09Z", c.date)
                ts.assertEquals("56ce52c7-a156-49ec-a826-128107e5a936",
                    c.id)
                # Comment via
                ts.assertEquals("http://github.com/", c.via.url)
                ts.assertEquals("GitHub", c.via.name)
                # Comment user
                ts.assertEquals("http://chan.friendfeed.com/kshep",
                    c.user.profileUrl)
                ts.assertEquals("kshep", c.user.nickname)
                ts.assertEquals("46958b7d-4bde-4890-8842-8cc33e8f55bd",
                    c.user.id)
                ts.assertEquals("Ken Sheppardson", c.user.name)
        ff = ffxml.Feed(D())

        f=open("test/sample.xml")
        d=f.read()
        f.close()

        ff.write(d)
        f.close()

    def testParsingMultiComment(self):
        # This needs to do something useful...
        ts=self
        class D(object):
            def gotUpdate(self, token, poll_interval, incomplete):
                ts.assertEquals('39180875991', token)
                ts.assertEquals('40', poll_interval)
                ts.assertEquals('False', incomplete)
            def gotEntry(self, e):
                ts.assertEquals("2008-11-03T19:43:09Z", e.updated)
                ts.assertEquals("Ken Sheppardson just committed a change to enjit on GitHub",
                    e.title)
                ts.assertEquals("True", e.is_new)
                ts.assertEquals("http://github.com/kshep/enjit/commit/dd3ed5a5421e465e2e2dee8130032eefaff29bb8",
                    e.link)
                ts.assertEquals("False", e.anonymous)
                ts.assertEquals("2008-11-03T19:43:09Z", e.published)
                ts.assertEquals("False", e.hidden)
                ts.assertEquals("0d751d07-a439-49a5-9c26-afda3d1fdea3", e.id)
                # Via
                ts.assertEquals("http://github.com/", e.via.url)
                ts.assertEquals("GitHub", e.via.name)
                # Service
                ts.assertEquals("http://friendfeed.com/", e.service.profileUrl)
                ts.assertEquals("http://chan.friendfeed.com/static/images/icons/internal.png?v=e471e9afdf04ae568dcbddb5584fc6c0",
                    e.service.iconUrl)
                ts.assertEquals("internal", e.service.id)
                ts.assertEquals("link", e.service.entryType)
                ts.assertEquals("FriendFeed", e.service.name)
                # User
                ts.assertEquals("http://chan.friendfeed.com/kshep",
                    e.user.profileUrl)
                ts.assertEquals("kshep", e.user.nickname)
                ts.assertEquals("46958b7d-4bde-4890-8842-8cc33e8f55bd",
                    e.user.id)
                ts.assertEquals("Ken Sheppardson", e.user.name)

                # Comment
                c=e.comments[0]
                ts.assertEquals("dd3ed5a5421e465e2e2dee8130032eefaff29bb8 - Fix for UnicodeEncodeError",
                    c.body)
                ts.assertEquals("True", c.is_new)
                ts.assertEquals("2008-11-03T19:43:09Z", c.date)
                ts.assertEquals("56ce52c7-a156-49ec-a826-128107e5a936", c.id)
                # Comment via
                ts.assertEquals("http://github.com/", c.via.url)
                ts.assertEquals("GitHub", c.via.name)
                # Comment user
                ts.assertEquals("http://chan.friendfeed.com/kshep",
                    c.user.profileUrl)
                ts.assertEquals("kshep", c.user.nickname)
                ts.assertEquals("46958b7d-4bde-4890-8842-8cc33e8f55bd",
                    c.user.id)
                ts.assertEquals("Ken Sheppardson", c.user.name)

                # Second Comment
                c=e.comments[1]
                ts.assertEquals("another comment", c.body)
                ts.assertEquals("True", c.is_new)
                ts.assertEquals("2008-11-03T20:43:09Z", c.date)
                ts.assertEquals("56ce52c7-a156-49ec-a826-128107e5a93x", c.id)
                # Comment via
                ts.assertEquals("http://github.com/2", c.via.url)
                ts.assertEquals("GitHub 2", c.via.name)
                # Comment user
                ts.assertEquals("http://chan.friendfeed.com/dlsspy",
                    c.user.profileUrl)
                ts.assertEquals("dlsspy", c.user.nickname)
                ts.assertEquals("46958b7d-4bde-4890-8842-8cc33e8f55bx",
                    c.user.id)
                ts.assertEquals("Dustin Sallings", c.user.name)
        ff = ffxml.Feed(D())

        f=open("test/sample-multi-comment.xml")
        d=f.read()
        f.close()

        ff.write(d)
        f.close()

    def testSample2(self):
        # This needs to do something useful...
        ts=self
        class D(object):
            def gotUpdate(self, token, poll_interval, incomplete):
                ts.assertEquals('39935774494', token)
                ts.assertEquals('40', poll_interval)
                ts.assertEquals('True', incomplete)
            def gotEntry(self, e):
                if e.id == 'e78e58c8-64a1-4462-a97c-891b27745789':
                    ts.assertEquals("The Ladner Report: Amazing: Obama Helped Stranded Stranger 20 Years Ago",
                        e.title)
        ff = ffxml.Feed(D())

        f=open("test/sample2.xml")
        d=f.read()
        f.close()

        ff.write(d)
        f.close()

    def testRoom(self):
        ts=self
        class D(object):
            def gotUpdate(self, token, poll_interval, incomplete):
                raise "Didn't expect an update."
            def gotEntry(self, e):
                if e.id == 'f1b516ab-55dc-5d60-44d7-676f7dff737c':
                    ts.assertEquals("True", e.anonymous)
                    ts.assertEquals("blogsunited", e.room.nickname)
                    ts.assertEquals("BlogsUnited", e.room.name)
                    ts.assertEquals("http://friendfeed.com/rooms/blogsunited",
                        e.room.url)
                    ts.assertEquals("fc1e3d84-07a7-4d7d-8074-453bf16c17a5",
                        e.room.id)
        ff = ffxml.Feed(D())

        f=open("test/public-sample.xml")
        d=f.read()
        f.close()

        ff.write(d)
        f.close()

    def testLike(self):
        ts=self
        class D(object):
            def gotUpdate(self, token, poll_interval, incomplete):
                raise "Didn't expect an update."
            def gotEntry(self, e):
                if e.id == 'd13b2be1-4964-44b1-bd9b-a713dc834328':
                    ts.assertEquals("False", e.anonymous)
                    ts.assertEquals("2008-11-10T04:29:08Z", e.likes[0].date)
                    ts.assertEquals("geekandahalf", e.likes[0].user.nickname)
                    ts.assertEquals("Derrick", e.likes[0].user.name)
                    ts.assertEquals("http://friendfeed.com/geekandahalf",
                        e.likes[0].user.profileUrl)
                    ts.assertEquals("0b04366e-7205-11dd-9e66-003048343a40",
                        e.likes[0].user.id)
        ff = ffxml.Feed(D())

        f=open("test/public-sample.xml")
        d=f.read()
        f.close()

        ff.write(d)
        f.close()

if __name__ == '__main__':
    unittest.main()
