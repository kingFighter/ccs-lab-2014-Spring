from flask import g, redirect, render_template, request, url_for, Markup
from functools import wraps
from debug import *
from zoodb import *

import auth_client
import bank_client
import honeychecker_client
import random

import rpclib

class User(object):
    def __init__(self):
        self.person = None

    def checkLogin(self, username, password):
        # token[0]:token token[1]:index
        token = auth_client.login(username, password)
        if token is not None:
            ret = honeychecker_client.check(username, token[1])
            if ret == 0:            # correct
                return self.loginCookie(username, token[0])
            elif ret == 2:
                '''
                honeywords, proceed by policy such as:
                1. setting o an alarm or notifying a system administrator,
                2. letting login proceed as usual,
                3. letting the login proceed, but on a honeypot system,
                4. tracing the source of the login carefully,
                5. turning on additional logging of the user's activities,
                6. shutting down that user's account until the user establishes a new password
                (e.g. by meeting with the sysadmin),
                7. shutting down the computer system and requiring
                all users to establish new passwords.

                Here we simply deny and log
                '''
                return None
        else:
            honeychecker_client.check(username, 0)
            return None

    def loginCookie(self, username, token):
        self.setPerson(username, token)
        return "%s#%s" % (username, token)

    def logout(self):
        self.person = None

    def addRegistration(self, username, password):
        # token[0]:token token[1]:index
        token = auth_client.register(username, password)

        if token is not None:
            bank_client.setup(username)
            honeychecker_client.set(username, token[1])
            return self.loginCookie(username, token[0])
        else:
            return None

    def checkCookie(self, cookie):
        if not cookie:
            return
        (username, token) = cookie.rsplit("#", 1)
        if auth_client.check_token(username, token):
            self.setPerson(username, token)

    def setPerson(self, username, token):
        persondb = person_setup()
        self.person = persondb.query(Person).get(username)
        self.token = token
        self.zoobars = bank_client.balance(username)

def logged_in():
    g.user = User()
    g.user.checkCookie(request.cookies.get("PyZoobarLogin"))
    if g.user.person:
        return True
    else:
        return False

def requirelogin(page):
    @wraps(page)
    def loginhelper(*args, **kwargs):
        if not logged_in():
            return redirect(url_for('login') + "?nexturl=" + request.url)
        else:
            return page(*args, **kwargs)
    return loginhelper

@catch_err
def login():
    cookie = None
    login_error = ""
    user = User()

    if request.method == 'POST':
        username = request.form.get('login_username')
        password = request.form.get('login_password')

        if 'submit_registration' in request.form:
            if not username:
                login_error = "You must supply a username to register."
            elif not password:
                login_error = "You must supply a password to register."
            else:
                cookie = user.addRegistration(username, password)
                if not cookie:
                    login_error = "Registration failed."
        elif 'submit_login' in request.form:
            if not username:
                login_error = "You must supply a username to log in."
            elif not password:
                login_error = "You must supply a password to log in."
            else:
                cookie = user.checkLogin(username, password)
                if not cookie:
                    login_error = "Invalid username or password."

    nexturl = request.values.get('nexturl', url_for('index'))
    if cookie:
        response = redirect(nexturl)
        ## Be careful not to include semicolons in cookie value; see
        ## https://github.com/mitsuhiko/werkzeug/issues/226 for more
        ## details.
        response.set_cookie('PyZoobarLogin', cookie)
        return response

    return render_template('login.html',
                           nexturl=nexturl,
                           login_error=login_error,
                           login_username=Markup(request.form.get('login_username', '')))

@catch_err
def logout():
    if logged_in():
        g.user.logout()
    response = redirect(url_for('login'))
    response.set_cookie('PyZoobarLogin', '')
    return response
