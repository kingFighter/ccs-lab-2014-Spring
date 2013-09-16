#!/bin/bash

SOCKET=/tmp/xsock

PASS="\033[1;32mPASS\033[m"
FAIL="\033[1;31mFAIL\033[m"

if [ -e "$SOCKET" ] ; then
    rm $SOCKET
fi

# launch the server.
./zoobar/rpctest-server.py 0 $SOCKET &>/dev/null &
server_pid=$!
need_cleanup=1

# wait until we can connect
sleep 1
if ! [ -e "$SOCKET" ] ; then
  echo "server did not create $SOCKET"
  exit 1
fi

# run the script with a 5-second timeout.
./zoobar/rpctest-client.py $SOCKET >/tmp/ex6.log 2>/dev/null &
pid=$!
(sleep 5; kill -9 $pid &>/dev/null) &
wait $pid

# stop the server.
kill -9 $server_pid &>/dev/null
wait $server_pid &> /dev/null

# check that we got a SIGSEGV.
if grep -Fxq PASS /tmp/ex6.log; then
  echo -e "$PASS Exercise 6"
else
  echo -e "$FAIL Exercise 6: see /tmp/ex6.log"
fi

