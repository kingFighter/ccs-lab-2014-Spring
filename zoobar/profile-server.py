#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import socket
import bank
import zoodb
import glob

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor
        os.chdir('/tmp')
        os.setgid(61012)
        os.setuid(61016)

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank.get_log(username):
            xfers.append({ 'sender': xfer.sender,
                           'recipient': xfer.recipient,
                           'amount': xfer.amount,
                           'time': xfer.time,
                         })
        return xfers

    def rpc_get_user_info(self, username):
        profile_db = zoodb.profile_setup()
        p = profile_db.query(zoodb.Profile).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': p.profile,
                 'zoobars': bank.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank.transfer(self.user, target, zoobars)

    def rpc_send_msg(self, msg):
        fn = '%s.%s' % (self.user, self.visitor)
        try:
            with open(fn, 'a') as f:
                f.write(str(time.time()) + " " + msg + "\n")
                f.close()
        except IOError, e:
            pass

    def rpc_get_msg(self):
        fns = glob.glob("*." + self.user)
        wels = {}
        
        for fn in fns:
            i = 0
            content = []
            with open(fn) as fp:
                for line in fp:
                    index = line.index(" ")
                    content.append(['time' + str(i), line[:index]])
                    content.append(['msg' + str(i), line[index + 1:]])
                    i = i + 1
            wels[fn.split(".")[0]] = content
        return wels

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        uid = 61018

        userdir = '/tmp'
        
        # let user know we will ignore '/', and '.' will be replaced
        # by '0'.
        # user name 'test/.' is the same as 'test0'
        user = user.replace("/", "")
        user = user.replace(".", "0")
        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)
        
        userdir = os.path.join(userdir, user)
        if not os.path.exists(userdir):
            os.mkdir(userdir)
            os.chmod(userdir, 0777)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
