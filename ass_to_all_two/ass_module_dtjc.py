# -*- coding: utf-8 -*-
__author__ = 'lihailin'

import sys
import os
import ass_base
import ass_config
from ass_module import AssModule
from androguard.core.androgen import AndroguardS
from androguard.core.analysis import analysis
from androguard.core.bytecodes.dvm import *
from ass_report import  AssReport
class AssD(AssModule):
    def run(self):



        self.adb("kill-server")
        #获取apk package name
        self.report.progress("获取包名")
        apk = ''
        ret = self.get_package_info()
        lines = ret.splitlines()
        if len(lines)>0:
            apk = ass_base.get_val(lines[0], "package: name='")
            apk = ass_base.get_val(apk, "' version", False)
        print "apk:"+apk
        #nam = input('waiting...')
        if apk == '':
            print(self.i18n('无法获取包名'))
            return 2

        #拿到android的root权限
        self.adb('remount')
        self.adb('push '+ ass_config.pinggu_dir+'/tool/su /system/xbin')
        self.adb('shell chmod 6777 /system/xbin/su')
        name = raw_input()

        pid = self.getpid_by_appname(apk)

        #设置模拟器检测
        maps_str = self.get_maps(pid)
        self.report.setItem('0_10', "app pid "+pid+ "; App package name "+apk+' ;maps '+ maps_str)
        maps_addrs = self.get_maps_addrs(maps_str)
        i = 0
        j = 9902
        self.adb('shell mkdir /data/data/maps')
        print 'mkdir '+ass_config.pinggu_dir+'/maps'
        self.do_cmd('mkdir '+ass_config.pinggu_dir+'/maps')
        #nam = input('waiting...')
        sstr = ''
        for addr in maps_addrs:
            if i>=5:
                break
            i+=1
            j+=1
            start_addr = '0x'+addr[0]
            #end_addr = '0x'+str(hex(start_addr)+180)
            end_addr = '0x'+addr[1]
            print start_addr
            print end_addr
            lines = self.drozer('run xv.operatemem -stt '+str(j)+' -sp '+pid+' --dump '+start_addr+' '+end_addr+' /data/data/maps/'+str(i)+'.txt')
            if('DUMP_FAIL' not in lines):
                #nam = input('waiting...')
                self.adb('pull /data/data/maps/'+str(i)+'.txt'+'  '+ass_config.pinggu_dir+'/maps')
                sstr += self.readfileby16(ass_config.pinggu_dir+'/maps/'+str(i)+'.txt',200)
        self.adb('shell rm -r /data/data/maps')
        print sstr
        #nam = input('waiting...')
        self.report.setItem('1_19', sstr)
        self.report.setItem('2_11', sstr)
        #nam = input('waiting...')
        pass
    def getpid_by_appname(self,appname):
        dict_pids = {}
        lines = self.drozer("run xv.operatemem -stt 9900 -ps 90")
        for line in lines:
            if 'process_name:' in line:
                line = line.replace('process_name:','')
                tm = line.split('pid:')
                dict_pids[tm[1]] = tm[0].strip()
        for pid in dict_pids.keys():
            #print pid
            #print dict_pids[pid]
            if dict_pids[pid] in appname:
                print pid
                print appname
                return pid
    def get_maps(self,pid):
        str1 = ''
        lines = self.drozer('run xv.operatemem -stt 9901  -ms 2 -sp '+str(pid))
        for line in lines:
            str1+=line+"|"
        #print str
        #nam = input('waiting...')
        return str1
    def get_maps_addrs(self,str1):
        rets = []
        lines = str1.split('|')
        for line in lines:
            if(line.strip()!= '' or line.strip()!='SUCCESS'):
                lis = line.strip().split(' ')
                if len(lis) < 5:
                    continue
                if('rw' in lis[1]):
                    rets.append(lis[0].split('-'))
        return  rets

    def readfileby16(self,filename,len_bt):
        str1 = ''
        f=open(filename,'rb')
        f.seek(0,0)
        index=0
        #for i in range(0,16):
            #print "%3s" % hex(i) ,
        #print
        #for i in range(0,16):
            #print "%-3s" % "#" ,
        #print
        len1 = 0
        while len1<len_bt:
            len1+=1
            temp=f.read(1)
            if len(temp) == 0:
                break
            else:
                #tmp = "%3s" % temp.encode('hex')
                tmp = temp.encode('hex')
                str1 += tmp
                #print tmp
                index=index+1
            if index == 16:
                index=0
                #print
        f.close()
        return str1
