from debug import *
from zoodb import *
import rpclib

sockname = "/banksvc/sock"
c = rpclib.client_connect(sockname)

def transfer(sender, recipient, zoobars, token):
    kwargs = {}
    kwargs['sender'] = sender
    kwargs['recipient'] = recipient
    kwargs['zoobars'] = zoobars
    kwargs['token'] = token
    return c.call('transfer', **kwargs)
    
def balance(username):
    kwargs = {}
    kwargs['username'] = username
    return c.call('balance', **kwargs)
            
def get_log(username):
    kwargs = {}
    kwargs['username'] = username
    return c.call('get_log', **kwargs)

def setup(username):
    kwargs = {}
    kwargs['username'] = username
    return c.call('setup', **kwargs)
            
