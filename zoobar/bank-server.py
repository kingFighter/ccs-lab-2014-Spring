#!/usr/bin/python

import rpclib
import sys
import bank
from debug import *
from sqlalchemy.orm import class_mapper
from pbkdf2 import crypt

def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_transfer(self, sender, recipient, zoobars, token):
        for (k, v) in token.items():
            if v != crypt(k, v):
                return
        return bank.transfer(sender, recipient, zoobars)
        
    def rpc_balance(self, username):
        return bank.balance(username)

    def rpc_get_log(self, username):
        serialized_labels = [
            serialize(label)
            for label in bank.get_log(username)
        ]
        return serialized_labels
        
    def rpc_setup(self, username):
        bank.setup(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)

