#!/bin/sh
DIR=$(cd "$(dirname "$0")"; pwd)
java -jar $DIR"/sign/signapktool.jar" $DIR"/sign/testkey.x509.pem" $DIR"/sign/testkey.pk8" $1 $2 $3 $4 $5 $6
