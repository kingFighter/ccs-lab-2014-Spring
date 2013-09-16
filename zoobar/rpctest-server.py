#!/usr/bin/python
##
## Run this server using something like:
##
##   ./rpctest-server.py 0 /tmp/xsock

import rpclib
import sys
import hashlib
from debug import *

def kw_sorted(kw):
    return sorted([[k, v] for (k, v) in kw.iteritems()])

class MyRpcServer(rpclib.RpcServer):
    def rpc_foo(self, a, b, c):
        print >>sys.stderr, 'running foo', a, b, c
        return 'bar'

    def rpc_hash(self, **kwargs):
        print >>sys.stderr, 'running hash', kwargs
        return hashlib.md5(str(kw_sorted(kwargs))).hexdigest()

    def rpc_echo(self, **kwargs):
        print >>sys.stderr, 'running echo', kwargs
        return kw_sorted(kwargs)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = MyRpcServer()
setattr(s, 'rpc_hash take\ntwo', MyRpcServer.rpc_hash.__get__(s, MyRpcServer))
s.run_sockpath_fork(sockpath)

