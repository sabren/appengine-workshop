"""
handy routines for python
"""
## TODO: break handy into submodules so it doesn't import everything under the sun

import re
import hashlib
import operator
import os
import random
import string
import tempfile
import urllib
import sys
import warnings

if sys.version_info[0]== 2:
    from htmlentitydefs import name2codepoint, entitydefs
else:
    from html.entities import name2codepoint, entitydefs
    from functools import reduce


try:
    from genshi.template.text import NewTextTemplate
    def genshiText(indented_string):
        t = NewTextTemplate(trim(indented_string))
        return lambda **kw: t.generate(**kw).render()
except ImportError: pass

try: from Ft.Xml.Domlette import NonvalidatingReader
except ImportError: pass

ZETTA = 10**21
EXA   = 10**18
PETA  = 10**15
TERA  = 10**12
GIGA  = 10**9
MEGA  = 10**6
KILO  = 10**3


def trim(s):
    """
    strips leading indentation from a multi-line string.
    for saving bandwidth while making code look nice
    """
    lines = string.split(s, "\n")

    # strip leading blank line
    if lines[0] == "":
        lines = lines[1:]

    # strip indentation
    indent = len(lines[0]) - len(string.lstrip(lines[0]))
    for i in range(len(lines)):
        lines[i] = lines[i][indent:]

    return string.join(lines, "\n")


def debug(password='abc123'):
    import rpdb2
    rpdb2.start_embedded_debugger(
        password, fAllowUnencrypted=True, fAllowRemote=True)


class switch(object):
    """
    syntactic sugar for multiple dispatch

    this idea is taken from:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/410692
    
    it's modified slightly because I didn't want
    the 'fall through' behavior that required break
    """
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        """
        this lets you do 'for case in switch()'
        """
        yield self.match
        raise StopIteration

    def match(self, *args):
        return self.value in args



#def daysInMonthPriorTo(day):
#    return (day - day.d).d
#
#
#def daysInLastMonth():
#    return daysInMonthPriorTo( Date("today"))



def randpass(length=5):
    okay = "abcdefghijkmnopqrstuvwxyz2345678923456789"
    res = ""
    for i in range(length+1):
        res += okay[random.randrange(0, len(okay))]
    return res


def reconcile(seriesA, seriesB):
    extraA = [x for x in seriesA if x not in seriesB]
    extraB = [x for x in seriesB if x not in seriesA]
    return extraA, extraB


def readable(bytes):
    """
    convert a byte count into human-readable text
    """
    x = bytes
    b = x % 1000; x-=b; x/=1000
    k = x % 1000; x-=k; x/=1000
    m = x % 1000; x-=m; x/=1000
    g = x % 1000; x-=g; x/=1000
    if g: return str(g) + "." + string.zfill(str(m),3)[0] + "G"
    if m: return str(m) + "." + string.zfill(str(k),3)[0] + "M"
    if k: return str(k) + "." + string.zfill(str(b),3)[0] + "k"
    return str(b)


def sendmail(mail):
    sender = os.popen("/usr/sbin/sendmail -t", "w")
    sender.write(mail)
    sender.close()


def trim(s):
    """
    strips leading indentation from a multi-line string.
    for saving bandwith while making code look nice
    """
    lines = string.split(s, "\n")

    # strip leading blank line
    if lines[0] == "":
        lines = lines[1:]

    # strip indentation
    indent = len(lines[0]) - len(string.lstrip(lines[0]))
    for i in range(len(lines)):
        lines[i] = lines[i][indent:]

    return string.join(lines, "\n")


def indent(s, depth=1, indenter="    "):
    """
    opposite of trim
    """
    lines = string.split(s, "\n")

    # don't indent trailing newline
    trailer = ""
    if lines[-1] == "":
        lines = lines[:-1]
        # BUT.. add it back in later
        trailer = "\n"

    for i in range(len(lines)):
        lines[i] = (indenter * depth) + lines[i]

    return string.join(lines, "\n") + trailer


def uid():
    """
    unique identifier generator, for sessions, etc
    Returns a 32 character, printable, unique string
    """
    tmp, uid = "", ""

    # first, just get some random numbers
    for i in range(64):
        tmp += chr(random.randint(0, 255))

    # then make a 16-byte md5 digest...
    tmp = hashlib.md5.new(tmp).digest()

    # and, since md5 is unprintable,
    # reformat it in hexadecimal:
    for i in tmp:
        uid += string.zfill(hex(ord(i))[2:],2)

    return uid


def edit(s):
    """
    launch an editor...
    """
    ed = os.environ.get("EDITOR", "vi")
    fn = tempfile.mktemp()
    tf = open(fn,"w")
    tf.write(s)
    tf.close()
    os.system("%s %s" % (ed, fn))
    return open(fn).read()



def sum(series, initial=None):
    return reduce(operator.add, series, 0)
assert sum((1,2,3)) == 6


class Everything(object):
    def __contains__(self, thing):
        return True
Everything=Everything()
assert 234324 in Everything



def deNone(s, replacement=''):
    """
    replaces None with the replacement string
    """
    # if s won't be zero, you might as well use:
    # "s or ''" instead of "deNone(s)"
    if s is None:
        return replacement
    else:
        return s


def urlDecode(what):
    if type(what) == type(""):
        res = urllib.unquote(string.replace(what, "+", " "))
    #elif type(what) == type({}):
    else:
        raise ValueError("urlDecode doesn't know how to deal with this kind of data")
    return res



def htmlEncode(s):
    _entitymap = dict((val, key) for (key,val) in entitydefs.items())
    has_entity = lambda ch: (ch in _entitymap or str(ch) in _entitymap)
    as_entity  = lambda ch: ("&" + _entitymap[ch] + ";") if has_entity(ch) else ch
    return ''.join(as_entity(ch) for ch in s)


# http://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django
def htmlDecode(s):
    """
    unescape HTML code refs; c.f. http://wiki.python.org/moin/EscapingHtml

    @param s:
    @return:
    """
    return re.sub('&(%s);' % '|'.join(name2codepoint),
        lambda m: unichr(name2codepoint[m.group(1)]), s)

def take(howMany, series):
    count = 0
    each = iter(series)
    while count < howMany:
        yield next(series)
        count += 1


def xml(s):
    """
    parse the xml and return a Ft.Xml.Domlette
    """
    return NonvalidatingReader.parseString(s)


def xmlEncode(s):
    """
    xmlEncode(s) ->  s with >, <, and & escaped as &gt;, &lt; and &amp;
    """
    res = ""
    for ch in s:
        if ch == ">":
            res += "&gt;"
        elif ch=="<":
            res += "&lt;"
        elif ch=="&":
            res += "&amp;"
        else:
            res = res + ch
    return res


class Proxy(object):
    def __init__(self, obj):
        self.__dict__['obj'] = obj

    def __getattr__(self, slot):
        return getattr(self.obj, slot)

    def __getitem__(self, slot):
        return self.obj[slot]

    def __setattr__(self, slot, value):
        setattr(self.obj, slot, value)

    def __setitem__(self, slot, value):
        self.obj[slot] = value

def typecheck(obj, typ):
    warnings.warn("use check module instead", DeprecationWarning)
    if isinstance(obj, typ):
        return obj
    else:
        raise TypeError("expected type: %s, got: %r" % (typ, obj))


