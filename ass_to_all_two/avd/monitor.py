# -*- coding: utf-8 -*-
import socket   #socketģ��
import commands   #ִ��ϵͳ����ģ��
import log_print
import traceback
import time  
import thread  
import subprocess
import signal,os,select 

from datetime import datetime

AVD_PROCESS_HANDLE = None
AVD_PROCESS_PID = 0;

def timer(HOST,PORT,avd_cmd):  
    ready_avd_env()
    log_print.LOG_OUT("start listen : %s %s " % (HOST,PORT));

    while 1:
        s = None
        conn = None
        try:
            s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #����socket���ͣ�����ͨ�ţ�TCP
            s.bind((HOST,PORT))   #�׽��ְ󶨵�IP��˿�
            s.listen(1)         #��ʼTCP����
            log_print.LOG_OUT("listen ok ....")
            while 1:
                log_print.LOG_OUT("[ accept commands ]")
                conn,addr=s.accept()   #����TCP���ӣ��������µ��׽�����IP��ַ
                data=conn.recv(1024)    #�ѽ��յ�����ʵ����
                log_print.LOG_OUT("recive data : %s"%data)
                if data.find("restart_avd") >=0:
                    while 1:
                        try:
                            log_print.LOG_OUT("restart avd ...")
                            pid = get_pid(avd_cmd) #��ȡ���������ID
                            log_print.LOG_OUT("kill : %s" %  pid)
                            #���������
                            cmd_exe("kill -9 %s"%pid)
                            #��⻷��
                            res = ready_avd_env()
                            if res == True:
                                break
                        except:
                            traceback.print_exc()

                    conn.sendall("open_ok")
                else:
                    conn.sendall("unknown")

                log_print.LOG_OUT("listen out ....")
                conn.close()     #�ر�����
        except:
            traceback.print_exc()
            log_print.LOG_OUT("listen out");
        #������Դ
        if s!=None :
            s.close()
        if conn!=None :
            conn.close()
    thread.exit_thread()  

#ִ��cmd linux ƽ̨֧�ֳ�ʱ
def handler(signum, frame):
    raise AssertionError

def cmd_exe(cmdline, timeout=300):#ִ��cmd
    t_start = datetime.now()
    log_print.LOG_OUT("[ CMD ] [%d] %s  " %(timeout,cmdline));
    pro = subprocess.Popen(cmdline, stdout=subprocess.PIPE,shell = True) 
    out =""
    while 1: 
        while_begin = time.time() 
        fs = select.select([pro.stdout], [], [], timeout) 
        if pro.stdout in fs[0]: 
            tmp = pro.stdout.read() 
            out = out + tmp
            if not tmp: 
                break 
        else: 
            out = 'timeout'
            os.kill(pro.pid, signal.SIGKILL)
            break 
        timeout = timeout - (time.time() - while_begin) 
    ##�������ִ��ʱ��
    log_print.LOG_OUT("[EXE TIME] %d secs" % ((datetime.now() - t_start).total_seconds()));
    log_print.LOG_OUT("[CMD OUT] %s" % out);
    return out


def open_avd(cmdline):#���������
    global AVD_PROCESS_PID
    global AVD_PROCESS_HANDLE
    log_print.LOG_OUT("avd open ...")
    log_print.LOG_OUT(cmdline);
    AVD_PROCESS_HANDLE = subprocess.Popen(cmdline, bufsize=0, shell=True, universal_newlines=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        AVD_PROCESS_PID = AVD_PROCESS_HANDLE.pid
        out,err = AVD_PROCESS_HANDLE.communicate()
        
    except AssertionError:
        AVD_PROCESS_HANDLE.terminate()
    log_print.LOG_OUT("avd close")

def split_empty(src, sep, index):
    srcs = src.split(sep)
    i = 0
    for dst in srcs:
        if dst=='':
            continue
#         print(i, dst)
        if i == index:
            return dst
        
        i=i+1
    
    return '' 

def get_pid( procName):#��ȡ����PID
    pids = cmd_exe("ps -ef | grep \""+procName+"\"").split("\n")
    len_procName = len(procName)
    for pid in pids:
        if pid[-len_procName:]==procName:
            return split_empty(pid, " ", 1)
    return ''

#�������Ҫ�������
def ready_avd_env():#������������  
    log_print.LOG_OUT("start drozer ...")
    
    time.sleep(20)
    while 1:
        out = cmd_exe("adb kill-server")
        cmd = "adb shell \"am start -n com.mwr.dz/com.mwr.dz.activities.MainActivity\""
        out = cmd_exe(cmd)
        if out.find("Starting: Intent")>=0:
            log_print.LOG_OUT("start drozer ok")
            #�ȴ�
            log_print.LOG_OUT("wait 10 secs end")
            time.sleep(10)
            return True
        elif out.find("device offline")>=0:
            return False
        else:
            #�ȴ�
            log_print.LOG_OUT("wait 10 secs to retry ...")
            time.sleep(10);
    return False

if __name__=="__main__": # �������

    HOST='127.0.0.1'
    PORT=4405
    #���������������
    avd_cmd = "/home/andro/tools/AndroidSdk/Sdk/tools//emulator @lab" 
    #avd_cmd = "/home/andro/tools/AndroidSdk/Sdk/tools/emulator -avd test" 
    #�����������������
    avd_procName = "/home/andro/Tools/AndroidSDK/Sdk/tools//emulator64-arm @lab"
    #avd_procName = "/home/andro/tools/AndroidSdk/Sdk/tools/emulator64-arm -avd test"
    thread.start_new_thread(timer, (HOST,PORT,avd_procName))  
    while 1:
        open_avd(avd_cmd)
    #HOST=config.server_ip
    #PORT=config.server_port
