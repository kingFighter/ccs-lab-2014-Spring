from debug import *
import logging
import os
from zoodb import *

def update(username, profile):
    db = profile_setup()
    pf = db.query(Profile).get(username)
    pf.profile = profile
    db.commit()

def setup(username):
    profiledb = profile_setup()
    newprofile = Profile()
    newprofile.username = username
    profiledb.add(newprofile)
    profiledb.commit()

def get(username):
    profiledb = profile_setup()
    pf = profiledb.query(Profile).get(username)
    return {'username': pf.username, 'profile': pf.profile}
