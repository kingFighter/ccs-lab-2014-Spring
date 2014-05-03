from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
from profile import *
import profilecharge_client
import bank_client

@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    if 'user' in request.values:
        persondb = person_setup()
        user = persondb.query(Person).get(request.values['user'])
        
        pf = profilecharge_client.get(user.username)
        if user:
            transferdb = transfer_setup()
            p = pf.profile
            if p.startswith("#!python"):
                p = run_profile(pf)

            p_markup = Markup("<b>%s</b>" % p)
            args['profile'] = p_markup
            args['user'] = user
            args['user_zoobars'] = bank_client.balance(user.username)
            args['transfers'] = bank_client.get_log(user.username)
        else:
            args['warning'] = "Cannot find that user."
    return render_template('users.html', **args)
