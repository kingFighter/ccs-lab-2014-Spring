from zoodb import *
from debug import *

import hashlib
import random
from pbkdf2 import PBKDF2
import os
import gen
import string

def newtoken(db, cred, i):
    hashinput = "%s%.10f" % (getattr(cred, 'password' + str(i)), random.random())
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

    for i in range(20):
        password_salt = PBKDF2(password, getattr(cred, 'salt' + str(i)), 2000).read(32)
        if getattr(cred, 'password' + str(i)) == password_salt.encode('base-64'):
            return (newtoken(creddb, cred, i), i + 1)

    # wrong pwd or pwd guessing
    return None

def register(username, password):
    persondb = person_setup()
    creddb = cred_setup()
    person = persondb.query(Person).get(username)

    if person:
        return None
    
    newperson = Person()
    newcred = Cred()
    newperson.username = username
    newcred.username = username

    # setup honeywords
    pw_list = gen.read_password_files({})
    passwords = gen.generate_passwords(19,pw_list)
    # avoid honeywords bump true password
    while passwords.count(password) > 0:
        passwords[passwords.index(password)] += ''.join(random.choice(string.lowercase) 
                                                        for i in range(5))
    passwords.append(password)
    random.shuffle(passwords)
    for i in range(20):
        salt = os.urandom(8)    # 64-bit salt
        setattr(newcred, 'salt' + str(i), salt.encode('base-64'))
        
        if passwords[i] == password:
            index = i + 1
        # 256-bit key
        passwords[i] = PBKDF2(passwords[i], getattr(newcred, 'salt' + str(i)),2000).read(32) 
        setattr(newcred, 'password' + str(i), passwords[i].encode('base-64'))

    persondb.add(newperson)
    creddb.add(newcred)

    persondb.commit()
    creddb.commit()
    
    return (newtoken(creddb, newcred, index - 1), index)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False
