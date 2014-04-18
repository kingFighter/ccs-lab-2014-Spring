from debug import *
import logging
import os
from zoodb import *

def set(username, index):
    db = honeychecker_setup()
    honeychecker = db.query(Honeychecker).get(username)
    if honeychecker:
        return None

    newhoneychecker = Honeychecker()
    newhoneychecker.username = username
    newhoneychecker.index = index
    db.add(newhoneychecker)
    db.commit()
    return True

# return value:
# 0 : password
# 1 : login deny
# 2 : honeywords
# 3 : no such username, though it won't happen
def check(username, index):
    # neither the password nor one of the users's honeywords
    # honeychecker is notied of every login attempt, and can observe
    # when a password guessing attack is in progress.
    if index == 0:
        logging.basicConfig(filename = os.path.join(os.getcwd(), 'honeycheckersvc',
                                                    'pwdGuess'),
                            level = logging.WARN,
                            filemode = 'a')

        logging.warning("Detect a password guessing attack.")
        return 1

    db = honeychecker_setup()
    honeychecker = db.query(Honeychecker).get(username)
    if not honeychecker:
        return 3
    
    if honeychecker.index == index:
        return 0
    else:
        # follow as policy
        # we just log it
        logging.basicConfig(filename = os.path.join(os.getcwd(), 'honeycheckersvc',
                                                    'warnAdversary'),
                            level = logging.WARN,
                            filemode = 'a')
        logging.warning("Detect an adversary.")
        return 2
    
