from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os
from debug import *

PersonBase = declarative_base()
CredBase = declarative_base()
TransferBase = declarative_base()
BankBase = declarative_base()
HoneycheckerBase = declarative_base()

class Person(PersonBase):
    __tablename__ = "person"
    username = Column(String(128), primary_key=True)
    profile = Column(String(5000), nullable=False, default="")

class Honeychecker(HoneycheckerBase):
    __tablename__ = "honeychecker"
    username = Column(String(128), primary_key=True)
    index = Column(Integer)

class Cred(CredBase):
    __tablename__ = "cred"
    username = Column(String(128), primary_key=True)
    # I don't know how to store arrays
    password0 = Column(String(128))
    salt0 = Column(String(128))
    password1 = Column(String(128))
    salt1 = Column(String(128))
    password2 = Column(String(128))
    salt2 = Column(String(128))
    password3 = Column(String(128))
    salt3 = Column(String(128))
    password4 = Column(String(128))
    salt4 = Column(String(128))
    password5 = Column(String(128))
    salt5 = Column(String(128))
    password6 = Column(String(128))
    salt6 = Column(String(128))
    password7 = Column(String(128))
    salt7 = Column(String(128))
    password8 = Column(String(128))
    salt8 = Column(String(128))
    password9 = Column(String(128))
    salt9 = Column(String(128))
    password10 = Column(String(128))
    salt10 = Column(String(128))
    password11 = Column(String(128))
    salt11 = Column(String(128))
    password12 = Column(String(128))
    salt12 = Column(String(128))
    password13 = Column(String(128))
    salt13 = Column(String(128))
    password14 = Column(String(128))
    salt14 = Column(String(128))
    password15 = Column(String(128))
    salt15 = Column(String(128))
    password16 = Column(String(128))
    salt16 = Column(String(128))
    password17 = Column(String(128))
    salt17 = Column(String(128))
    password18 = Column(String(128))
    salt18 = Column(String(128))
    password19 = Column(String(128))
    salt19 = Column(String(128))
    password20 = Column(String(128))
    salt20 = Column(String(128))
    token = Column(String(128))

class Transfer(TransferBase):
    __tablename__ = "transfer"
    id = Column(Integer, primary_key=True)
    sender = Column(String(128))
    recipient = Column(String(128))
    amount = Column(Integer)
    time = Column(String)

class Bank(BankBase):
    __tablename__ = "bank"
    username = Column(String(128), primary_key=True)
    zoobars = Column(Integer, nullable=False, default=10)

def dbsetup(name, base):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    dbdir   = os.path.join(thisdir, "db", name)
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)

    dbfile  = os.path.join(dbdir, "%s.db" % name)
    engine  = create_engine('sqlite:///%s' % dbfile)
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()

def person_setup():
    return dbsetup("person", PersonBase)

def cred_setup():
    return dbsetup("cred", CredBase)

def transfer_setup():
    return dbsetup("transfer", TransferBase)

def bank_setup():
    return dbsetup("bank", BankBase)

def honeychecker_setup():
    return dbsetup("honeychecker", HoneycheckerBase)

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [init-person|init-transfer|init-cred|init-bank|init-honeychecker]" % sys.argv[0]
        exit(1)

    cmd = sys.argv[1]
    if cmd == 'init-person':
        person_setup()
    elif cmd == 'init-cred':
        cred_setup()
    elif cmd == 'init-transfer':
        transfer_setup()
    elif cmd == 'init-bank':
        bank_setup()
    elif cmd == 'init-honeychecker':
        honeychecker_setup()
    else:
        raise Exception("unknown command %s" % cmd)
