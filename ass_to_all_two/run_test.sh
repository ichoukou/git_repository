#!/bin/sh
export JAVA_HOME=/usr/lib/jvm/java-7-sun
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
export PATH=${MAVEN_HOME}/bin:$PATH
export PATH=/usr/local/bin/linux_utils:$PATH
export PATH=/usr/lib/python2.7:$PATH

cd /home/anpro/test && python ./run_test.py
