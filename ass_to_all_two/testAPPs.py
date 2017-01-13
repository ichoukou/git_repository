#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import chardet
from threading import Timer

global t

def to_kill(p):
    if not p==None:
        p.terminate()
        
        
def do_cmd(cmdline, print_out=True, timeout=0):
    print(cmdline)
    p=subprocess.Popen(cmdline, bufsize = 0, shell=True, universal_newlines=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if timeout>0:
        t = Timer(timeout, to_kill(p))
        t.start()
    out = ''
    err = ''
    try:
        out,err = p.communicate()
    except:
        out = ''
        err = ''
        
    if print_out:
        print(out)
        
    if timeout>0:
        t.cancel()
        
    return out

def runTest(idx):
	f = open("/home/phyman/Lab/apk17/dirs", "r")
	i = 1
	while True:
		line = f.readline()
		if line:
			#print 'path =>' + line
			cmd = "python ass.py \"/home/phyman/Lab/apk17" + line.strip() + "\"" + ' > ' + "\"" + '/home/phyman/Lab/logs/' + str(idx) + '_' + line[line.rindex('/') + 1:].strip() + '.log'  + "\""
			#print 'before +++' + cmd
			#codeRet = chardet.detect(cmd)
			#print codeRet
			#cmd.decode(codeRet['encoding']).encode('utf-8')GB2312
			#cmd = cmd.decode('GB2312').encode('utf-8')
			#print 'after +++' + cmd
			print str(idx) + '@' + cmd
			#subprocess.call(cmd, shell = True)
			do_cmd(cmd)
		else:
			break
		i = i + 1
	f.close()

runTest(0)
#runTest(1)
