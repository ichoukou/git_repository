# -*- coding:utf-8 -*-
'''
'''

import subprocess
import os
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

is_running = do_cmd('ps awx|grep /home/anpro/AutoPacker/main.py|grep -v grep')
if len(is_running)>10:
    print("running:"+is_running)
    exit()

in_dir = '/home/anpro/test/jg_in/'
out_dir ='/home/anpro/test/jg_out/'     
files = os.listdir(in_dir)
if len(files)==0:
    print("no files in jg_in")
for file in files:
    if not os.path.exists(out_dir+file):
        os.system("python /home/anpro/jg/AutoPacker/main.py \""+in_dir+file+"\" \""+out_dir+file+"\"")
    else:
        os.chmod(out_dir+file, 0777)

