import rpclib
from debug import *
from collections import namedtuple

sockname = "/profilechargesvc/sock"
c = rpclib.client_connect(sockname)

def update(username, profile, token):
    kwargs = {}
    kwargs['username'] = username
    kwargs['profile'] = profile
    kwargs['token'] = token
    return c.call('update', **kwargs)

def setup(username):
    kwargs = {}
    kwargs['username'] = username
    return c.call('setup', **kwargs)

def get(username):
    kwargs = {}
    kwargs['username'] = username
    
    pf_dict = c.call('get', **kwargs)
    pfStruct = namedtuple('pfStruct', 'username profile')
    pf = pfStruct(username = pf_dict['username'], profile = pf_dict['profile'])

    return pf
    
