#!/usr/bin/python

import rpclib
import sys
from debug import *
import profilecharge
from pbkdf2 import crypt

# As described in Challenge, we only need to protect user profiles
# from modifying by attackers
# profile-server needs to read profile code directly, so we don't need
# to protect user profiles from reading by others and all the 'rpc'
# can be replaced by reading directly.

class ProfileChargeRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_update(self, username, profile, token):
        for (k, v) in token.items():
            if v != crypt(k, v):
                return
        return profilecharge.update(username, profile)

    def rpc_setup(self, username):
        return profilecharge.setup(username)
        
    def rpc_get(self, username):
        return profilecharge.get(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileChargeRpcServer()
s.run_sockpath_fork(sockpath)
