#!/bin/sh
DIR=$(cd "$(dirname "$0")"; pwd)
jdb -connect "com.sun.jdi.SocketAttach:hostname=localhost,port=6002"
