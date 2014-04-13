#!/usr/bin/python

import rpclib
import sys
from debug import *
import honeychecker

class HoneycheckerRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_set(self, username, index):
        return honeychecker.set(username, index)
        
    def rpc_check(self, username, index):
        return honeychecker.check(username, index)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = HoneycheckerRpcServer()
s.run_sockpath_fork(sockpath)
