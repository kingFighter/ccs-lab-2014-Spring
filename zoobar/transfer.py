from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bank_client
import traceback
import rpclib
from pbkdf2 import crypt

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            zoobars = eval(request.form['zoobars'])
            bank_client.transfer(g.user.person.username, request.form['recipient'], zoobars,
                              {g.user.token: crypt(g.user.token)})   
            
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError, NameError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
