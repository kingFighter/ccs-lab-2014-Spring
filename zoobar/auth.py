from zoodb import *
from debug import *

import hashlib
import random
from pbkdf2 import PBKDF2
import os


def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    persondb = person_setup()
    person = persondb.query(Person).get(username)
    if not person:
        return None
    
    creddb = cred_setup()
    cred = creddb.query(Cred).get(username)
    if not cred:
        return None
    
    password = PBKDF2(password, cred.salt, 2000).read(32)
    if cred.password == password.encode('base-64'):
        return newtoken(creddb, cred)
    else:
        return None

def register(username, password):
    persondb = person_setup()
    creddb = cred_setup()
    bankdb = bank_setup()
    person = persondb.query(Person).get(username)

    if person:
        return None

    newperson = Person()
    newcred = Cred()
    newbank = Bank()
    newperson.username = username
    newcred.username = username
    newbank.username = username
    salt = os.urandom(8)    # 64-bit salt
    newcred.salt = salt.encode('base-64')
    password = PBKDF2(password, newcred.salt, 2000).read(32) # 256-bit key
    newcred.password = password.encode('base-64')

    persondb.add(newperson)
    creddb.add(newcred)
    bankdb.add(newbank)
    persondb.commit()
    creddb.commit()
    bankdb.commit()

    return newtoken(creddb, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

