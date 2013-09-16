#!/usr/bin/python

import rpclib_orig
import sys
import os
from debug import *

class EchoRpcServer(rpclib_orig.RpcServer):
    def rpc_echo(self, s):
        return 'You said: %s' % s

    def rpc_unlink(self, pn):
        os.unlink(pn)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = EchoRpcServer()
s.run_sockpath_fork(sockpath)

