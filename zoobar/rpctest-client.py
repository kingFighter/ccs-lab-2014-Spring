#!/usr/bin/python
##
## Run this client using something like:
##
##   ./zoobar/rpctest-client.py /tmp/xsock

import rpclib
import sys
import hashlib
import string
import random
import traceback
from debug import *

(progname, sockname) = sys.argv
failed = False

def kw_sorted(kw):
    return sorted([[k, v] for (k, v) in kw.iteritems()])

def call_check(c, method, kwargs, expect):
    print "Invoking %s.." % method,
    try:
        r = c.call(method, **kwargs)
    except:
        traceback.print_exc(None, sys.stdout)
        r = None
    if r == expect:
        print "ok"
    else:
        global failed
        failed = True
        print "fail"
        print "Failing args:", kwargs
        print "Received:", type(r), r
        print "Expected:", type(expect), expect

def test_simple(c):
    call_check(c, 'foo', {'a': 1, 'b': 2, 'c': 3}, 'bar')
    call_check(c, 'foo', {'a': 99991, 'b': 99992, 'c': 99993}, 'bar')

def gen_string(alphabet, length=10):
    return u''.join(random.choice(alphabet) for _ in range(length))

def gen_args(alphabet):
    args = {}
    for _ in range(5):
        args[gen_string(alphabet)] = gen_string(alphabet)
    return args

def hash(args):
    return hashlib.md5(str(kw_sorted(args))).hexdigest()

def echo(args):
    return kw_sorted(args)

def test_random(c, func, expect, alphabet):
    for _ in range(20):
        args = gen_args(alphabet)
        call_check(c, func, args, expect(args))

def test_random_types(c, func, expect, choices):
    for _ in range(20):
        args = {}
        for _ in range(5):
            args[gen_string(string.ascii_letters)] = random.choice(choices)
        call_check(c, func, args, expect(args))

with rpclib.client_connect(sockname) as c:
    print 'Testing simple RPC..'
    test_simple(c)

    for func, expect in (('hash', hash), ('echo', echo),):
        print 'Testing alphanumerics..'
        alphabet = string.ascii_letters + string.digits
        test_random(c, func, expect, alphabet)

        print 'Testing punctuation..'
        alphabet += string.punctuation
        test_random(c, func, expect, alphabet)

        print 'Testing whitespace..'
        alphabet += string.whitespace
        test_random(c, func, expect, alphabet)

        print 'Testing all ASCII characters..'
        alphabet = [chr(x) for x in range(128)]
        test_random(c, func, expect, alphabet)

    print 'Testing method names..'
    test_random(c, 'hash take\ntwo', hash, string.ascii_letters + string.whitespace)

    print 'Testing None, bools, integers, dicts, lists..'
    test_random_types(c, 'echo', echo, (True, False,
                                        None,
                                        1, 2, 3,
                                        {u'a': 123, u'75': True},
                                        [u'Hello', u'22', 23, False]))

if failed:
    print "FAIL"
    sys.exit(1)
else:
    print "PASS"
    sys.exit(0)

