from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
from profile import *
import bank

sockname = "/banksvc/sock"
c = rpclib.client_connect(sockname)

@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    if 'user' in request.values:
        persondb = person_setup()
        user = persondb.query(Person).get(request.values['user'])
        if user:
            transferdb = transfer_setup()
            p = user.profile
            if p.startswith("#!python"):
                p = run_profile(user)

            p_markup = Markup("<b>%s</b>" % p)
            args['profile'] = p_markup

            args['user'] = user
            
            kwargs = {}
            kwargs['username'] = user.username
            args['user_zoobars'] = c.call('balance', **kwargs)
            args['transfers'] = c.call('get_log', **kwargs)
            
        else:
            args['warning'] = "Cannot find that user."
    return render_template('users.html', **args)
