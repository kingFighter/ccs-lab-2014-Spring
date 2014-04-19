import os
import sys
import socket
import stat
import errno
import json
import time
from debug import *

def parse_req(req):
    words = json.loads(req)
    
    for (method, args) in words.items():
        pass
    kwargs = {}
    for (name, val) in args.items():
        kwargs[unicode(name)] = val
    return (method, kwargs)

def format_req(method, kwargs):
    rep = {}
    rep[method] = kwargs
    return json.dumps(rep)

def parse_resp(resp):
    return json.loads(resp)

def format_resp(resp):
    return json.dumps(resp)

def buffered_readlines(sock):
    buf = ''
    while True:
        while '\n' in buf:
            (line, nl, buf) = buf.partition('\n')
            yield line
        try:
            newdata = sock.recv(4096)
            if newdata == '':
                break
            buf += newdata
        except IOError, e:
            if e.errno == errno.ECONNRESET:
                break

class RpcServer(object):
    def run_sock(self, sock):
        lines = buffered_readlines(sock)
        for req in lines:
            (method, kwargs) = parse_req(req)
            m = self.__getattribute__('rpc_' + method)
            ret = m(**kwargs)
            sock.sendall(format_resp(ret) + '\n')

    def run_sockpath_fork(self, sockpath):
        if os.path.exists(sockpath):
            s = os.stat(sockpath)
            if not stat.S_ISSOCK(s.st_mode):
                raise Exception('%s exists and is not a socket' % sockpath)
            os.unlink(sockpath)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(sockpath)

        # Allow anyone to connect.
        # For access control, use directory permissions.
        os.chmod(sockpath, 0777)

        server.listen(5)
        while True:
            conn, addr = server.accept()
            pid = os.fork()
            if pid == 0:
                # fork again to avoid zombies
                if os.fork() <= 0:
                    self.run_sock(conn)
                    sys.exit(0)
                else:
                    sys.exit(0)
            conn.close()
            os.waitpid(pid, 0)

class RpcClient(object):
    def __init__(self, sock):
        self.sock = sock
        self.lines = buffered_readlines(sock)

    def call(self, method, **kwargs):
        self.sock.sendall(format_req(method, kwargs) + '\n')
        return parse_resp(self.lines.next())

    def close(self):
        self.sock.close()

    ## __enter__ and __exit__ make it possible to use RpcClient()
    ## in a "with" statement, so that it's automatically closed.
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

def client_connect(pathname):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    while not os.path.exists(pathname): # wait program to create sock
        time.sleep(0.5)
    sock.connect(pathname)
    return RpcClient(sock)

