from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bank
import traceback
import rpclib
from pbkdf2 import crypt

sockname = "/banksvc/sock"
c = rpclib.client_connect(sockname)

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            zoobars = eval(request.form['zoobars'])
            kwargs = {}
            kwargs['sender'] = g.user.person.username;
            kwargs['recipient'] = request.form['recipient']
            kwargs['zoobars'] = zoobars
            kwargs['token'] = {g.user.token: crypt(g.user.token)}
            c.call('transfer', **kwargs)
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError, NameError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
