from flask import g, render_template, request
from login import requirelogin
from debug import *
from zoodb import *
import profilecharge_client
from pbkdf2 import crypt

@catch_err
@requirelogin
def index():
    if 'profile_update' in request.form:
        profilecharge_client.update(g.user.person.username, request.form['profile_update'], 
                                    {g.user.token: crypt(g.user.token)})
        ## also update the cached version (see login.py)
        g.user.person.profile = request.form['profile_update']

    return render_template('index.html')
