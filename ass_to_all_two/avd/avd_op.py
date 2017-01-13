# -*- coding: utf-8 -*-
import socket
import traceback

if __name__=="__main__": # 程序入口
    HOST='127.0.0.1'
    PORT=4405
    s = None;
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
        s.connect((HOST,PORT))       #要连接的IP与端口
        s.sendall("restart_avd2")      #把命令发送给对端
        data=s.recv(1024)     #把接收的数据定义为变量
        print data         #输出变量
        s.close()   #关闭连接
        #while 1:
        #    cmd=raw_input("Please input cmd:")       #与人交互，输入命令
        #    if cmd.find("out") >=0:
        #        break
        #    s.sendall(cmd)      #把命令发送给对端
        #    data=s.recv(1024)     #把接收的数据定义为变量
        #    print data         #输出变量
        #s.close()   #关闭连接
    except:
        traceback.print_exc()
    if s != None:
        s.close()