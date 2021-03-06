from twisted.internet import error
from twisted.web import sux

class NoopParser(object):
    def __init__(self, n):
        self.name = n
        self.done = False
    def gotTagStart(self, name):
        pass
    def gotTagEnd(self, name, data):
        self.done = (name == self.name)

class BaseXMLHandler(object):

    SIMPLE_PROPS = []
    COMPLEX_PROPS = {}
    tag_name = None

    def __init__(self):
        self.done = False
        self.current_ob = None
        for p in self.SIMPLE_PROPS:
            self.__dict__[p] = None

    def gotTagStart(self, name):
        if self.current_ob:
            self.current_ob.gotTagStart(name)
        elif name in self.COMPLEX_PROPS:
            self.current_ob = self.COMPLEX_PROPS[name]()
        elif name in self.SIMPLE_PROPS:
            pass
        else:
            self.current_ob = NoopParser(name)

    def gotTagEnd(self, name, data):
        if self.current_ob:
            self.current_ob.gotTagEnd(name, data)
            if self.current_ob.done:
                if name in self.COMPLEX_PROPS:
                    self.__dict__[name] = self.current_ob
                self.current_ob = None
        elif name == self.tag_name:
            self.done = True
            del self.current_ob
        elif name in self.SIMPLE_PROPS:
            self.__dict__[name] = data

    def __repr__(self):
        return "{%s %s}" % (self.tag_name, self.__dict__)

class Room(BaseXMLHandler):

    SIMPLE_PROPS = ['url', 'nickname', 'id', 'name']
    tag_name = 'room'

class Via(BaseXMLHandler):

    SIMPLE_PROPS = ['url', 'name']
    tag_name = 'via'

class Service(BaseXMLHandler):

    SIMPLE_PROPS = ['profileUrl', 'iconUrl', 'id', 'entryType', 'name']
    tag_name = 'service'

class User(BaseXMLHandler):

    SIMPLE_PROPS = ['profileUrl', 'nickname', 'id', 'name']
    tag_name = 'user'

class Comment(BaseXMLHandler):

    SIMPLE_PROPS = ['body', 'is_new', 'date', 'id']
    COMPLEX_PROPS = {'via': Via, 'user': User}
    tag_name = 'comment'

class Like(BaseXMLHandler):

    SIMPLE_PROPS = ['date']
    COMPLEX_PROPS = {'user': User}
    tag_name = 'like'

class Entry(BaseXMLHandler):

    SIMPLE_PROPS = ['updated', 'title', 'is_new', 'link', 'anonymous',
        'published', 'hidden', 'id']
    COMPLEX_PROPS = {'via': Via, 'service': Service, 'comment': Comment,
        'user': User, 'room': Room, 'like': Like}

    def __init__(self):
        super(Entry, self).__init__()
        self.comments=[]
        self.likes=[]

    def gotTagEnd(self, name, data):
        super(Entry, self).gotTagEnd(name, data)
        if name == 'comment':
            self.comments.append(self.comment)
            del self.comment
        elif name == 'like':
            self.likes.append(self.like)
            del self.like

    tag_name = 'entry'

class Feed(sux.XMLParser):

    """A file-like thingy that parses a friendfeed feed with SUX."""
    def __init__(self, delegate):
        self.delegate=delegate

        self.connectionMade()
        self.currentEntry=None
        self.data=[]

        self.token=None
        self.poll_interval=None
        self.incomplete=None
    def write(self, b):
        self.dataReceived(b)
    def close(self):
        self.connectionLost(error.ConnectionDone())
    def open(self):
        pass
    def read(self):
        return None

    # XML Callbacks
    def gotTagStart(self, name, attrs):
        self.data=[]
        if name ==  'entry':
            self.currentEntry = Entry()
        elif self.currentEntry:
            self.currentEntry.gotTagStart(name)

    def gotTagEnd(self, name):
        if name in ['token', 'poll_interval', 'incomplete']:
            self.__dict__[name] = ''.join(self.data)
        elif name == 'update':
            self.delegate.gotUpdate(self.token, self.poll_interval,
                self.incomplete)
        elif name == 'entry':
            self.currentEntry.done = True
            del self.currentEntry.current_ob
            self.delegate.gotEntry(self.currentEntry)
            self.currentEntry = None
        elif self.currentEntry:
            self.currentEntry.gotTagEnd(name, ''.join(self.data).decode('utf8'))

    def gotText(self, data):
        self.data.append(data)

    def gotEntityReference(self, data):
        e = {'quot': '"', 'lt': '&lt;', 'gt': '&gt;', 'amp': '&amp;'}
        if e.has_key(data):
            self.data.append(e[data])
        else:
            print "Unhandled entity reference: ", data
