# -*- coding: utf-8 -*-
import socket
import traceback

if __name__=="__main__": # �������
    HOST='127.0.0.1'
    PORT=4405
    s = None;
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #����socket���ͣ�����ͨ�ţ�TCP
        s.connect((HOST,PORT))       #Ҫ���ӵ�IP��˿�
        s.sendall("restart_avd2")      #������͸��Զ�
        data=s.recv(1024)     #�ѽ��յ����ݶ���Ϊ����
        print data         #�������
        s.close()   #�ر�����
        #while 1:
        #    cmd=raw_input("Please input cmd:")       #���˽�������������
        #    if cmd.find("out") >=0:
        #        break
        #    s.sendall(cmd)      #������͸��Զ�
        #    data=s.recv(1024)     #�ѽ��յ����ݶ���Ϊ����
        #    print data         #�������
        #s.close()   #�ر�����
    except:
        traceback.print_exc()
    if s != None:
        s.close()