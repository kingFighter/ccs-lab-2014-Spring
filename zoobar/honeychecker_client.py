import rpclib
from debug import *

sockname = "/honeycheckersvc/sock"
c = rpclib.client_connect(sockname)

def set(username, index):
    kwargs = {}
    kwargs['username'] = username
    kwargs['index'] = index
    return c.call('set', **kwargs)

def check(username, index):
    kwargs = {}
    kwargs['username'] = username
    kwargs['index'] = index
    return c.call('check', **kwargs)
