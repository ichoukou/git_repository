# -*- coding:utf-8 -*-

'''
'''

import sys
import os
from ass_module import AssModule
import ass_config
import time
from PIL import Image 
import math
import operator
from functools import reduce
from ass_base import q, rmdir, ass_mkdir, remove, write_file
import shutil
from _datetime import datetime
from ftplib import FTP

# cmd_inforce = "d:\\drozer\\python E:\\coralsec\\trunk\\reinforce\\script\\AutoPacker_no_enc\\main.py"
ftp_server   = "221.203.255.255"  
ftp_port     = "21"  
ftp_user     = "anprotestuser"  
ftp_password = "fafggs7687%^$%Asd"  

#加固测试接口
class AssTestInforce(AssModule):
    def init(self, argv):
        super(AssTestInforce, self).init(argv)
        self.report.report.test = {}
        
        self.out_file = ''
        self.csv = ''
        self.csv_head = ''
        
        if len(argv)>3:
            self.out_file = argv[3]
        
        return True
    #连接结构
    #[apk_file apk文件路径] [dest 目标文件]
    def inforce_begin(self, apk_file, dest): 
        # ftp settings
        filename = os.path.split(apk_file)[1]

        ftp = FTP(ftp_server, ftp_user, ftp_password)
        ftp.debug(1)  
        ftp.getwelcome() 
        ftp.cwd("test/jg_tmp") 
        ftp.storbinary("STOR "+filename, open(apk_file, "rb"), 1024)
        ftp.rename(filename, "../jg_in/"+filename)
        ftp.close()          
    
    def inforce_end(self, apk_file, dest):
        filename = os.path.split(apk_file)[1]
        
        ftp = FTP(ftp_server, ftp_user, ftp_password)  
        ftp.getwelcome()
        ftp.debug(1) 
        ftp.cwd("test/jg_out") 
        f = open(dest+".tmp", 'wb')  
        ftp.retrbinary("RETR "+filename, f.write , 1024)
        f.close()
        
        ftp.delete(filename)
        ftp.delete("../jg_in/"+filename)
        ftp.close()

        self.do_cmd(ass_config.cmd_sign+" "+q(dest+".tmp")+" "+q(dest))
        remove(dest+".tmp")
        
    def pil_image_similarity(self, filepath1, filepath2):
        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)
    
    #    image1 = get_thumbnail(img1)
    #    image2 = get_thumbnail(img2)
    
        h1 = image1.histogram()
        h2 = image2.histogram()
    
        rms = math.sqrt( reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
        return rms
                              
    def local_cap_file(self, apk_file, step, file):
        return os.path.join(apk_file+".png", step+self.get_screencap_file(file))
    
    def cap(self, apk_file, apk, step, files):
        for i in range(20):
            files.append(self.screnncap_one())
        
        pid = self.get_pid(apk)
        
        last_min = 100
        last_i = 0    
        for i in range(len(files)):
            f = files[i]
            
            if last_min>10 or i<last_i+1:
                self.adb("pull /data/"+self.get_screencap_file(f)+" "+q(self.local_cap_file(apk_file, step, f)))
            self.adb("shell rm /data/"+self.get_screencap_file(f))
            
            if i>0 and last_min>10:
                nmin = self.pil_image_similarity(self.local_cap_file(apk_file, step, files[i-1]), self.local_cap_file(apk_file, step, f))
                if nmin < last_min:
                    last_min = nmin
                    last_i = i
            
        return files[0], files[last_i], pid

    def run_apk_png(self, apk_file, apk, activity, step):
        files = []
        files.append(self.screnncap_one())
        self.start_apk(apk, activity)
        return self.cap(apk_file, apk, step, files)
        
    def run_apk_log(self, apk_file, apk, activity):
        self.start_apk(apk, activity)
        return self.adb("logcat", 10)
    
    def get_time(self, f):
#         return f.microseconds()
        return 1000* (f[0]*3600+f[1]*60+f[2])+(f[3]/1000)
            
    def run_apk_times(self, apk_step, apk_file, apk, activity, step):
        f, n, pid = self.run_apk_png(apk_file, apk, activity, step)
        start_time = self.get_time(n)-self.get_time(f)
        self.report.report.test[apk_step][step+'run'] = {'start':f, 'end':n, 'pid':pid, 'start_time':start_time}
        self.csv_head += ","+step+"启动时间,pid"
        self.csv += ",%d,%s" % (start_time, pid)
        self.adb("shell am kill-all")
        time.sleep(2)

    def run_apk(self, step, apk_file, apk, activity, first_uninstall=False):
        self.report.report.test[step] = {}
        size = 0
        if os.path.exists(apk_file):
            size = os.path.getsize(apk_file)
        
        self.report.report.test[step]['filesize'] = size
        self.csv_head += ","+step+':文件大小' 
        self.csv += ",%d"%size
        
        if first_uninstall:
            self.uninstall(apk)
        if self.install(apk_file):
            self.report.report.test[step]['install'] = True
            self.csv_head += ",安装"
            self.csv+=",True"
            
            ass_mkdir(apk_file+".png")
        
            self.run_apk_times(step, apk_file, apk, activity, "first_")
            self.run_apk_times(step, apk_file, apk, activity, "second_")

            self.report.report.test[step]['logcat'] = self.run_apk_log(apk_file, apk, activity)
            
            self.csv_head+=",卸载"
            if self.uninstall(apk).find("Success")>=0:
                self.report.report.test[step]['uninstall'] = True
                self.csv += ",True"
            else:
                self.report.report.test[step]['uninstall'] = False
                self.csv += ",False"
            
        else:
            self.report.report.test[step]['install'] = False
            self.csv_head += ",安装,first_启动时间,pid,second_启动时间,pid,卸载"
            self.csv+=",False,-,-,-,-,-"
    
    def resign(self, apk_file, dest):
        shutil.copyfile(apk_file, dest+".tmp")
        self.do_cmd(ass_config.cmd_7za+" d -tzip " + q(dest+".tmp")+" META-INF")
        if os.path.exists(dest+".tmp"):
            self.do_cmd(ass_config.cmd_sign+" "+q(dest+".tmp")+" "+q(dest))
            remove(dest+".tmp")
            if os.path.exists(dest):
                return True
        
        return False
    
    def run_test(self, apk, ver, label, activity):
        self.inforce_begin(self.apk_file, self.apk_file+".inforce")
        
        self.csv_head += "文件,包名,版本,应用名"
        self.csv = self.apk_file+","+apk+","+ver+",\""+label+"\""
        
#         1. 安装并运行原包，截图看成功和时间，如果有log更好
        self.run_apk("origin", self.apk_file, apk, activity, True)
         
#         2. 重新签名运行
        self.resign(self.apk_file, self.apk_file+".resign")
        self.run_apk("resign", self.apk_file+".resign", apk, activity, True)
#         
#         3. 加固运行
        self.inforce_end(self.apk_file, self.apk_file+".inforce")
        self.run_apk("inforce", self.apk_file+".inforce", apk, activity, True)        
        
        self.csv_head += "\n"
        self.csv += "\n"

    def run(self):
        super(AssTestInforce, self).run()
        self.connect_adb()
        
        try:
            apk, ver, label = self.get_package_base_info()
            activity = self.get_launchable_activity()
            
            if len(apk)>0:
                self.run_test(apk, ver, label, activity)
                if len(self.out_file)>0:
                    if not os.path.exists(self.out_file):
                        write_file(self.out_file, self.csv_head)
                    write_file(self.out_file, self.csv, 'a')
            else:
                write_file(self.out_file, self.apk_file+",-\n", "a")
                self.report.report.test = {'origin':{'apk':'is error'}}
        except:
            write_file(self.out_file, self.apk_file+",-\n", "a")
            
        delattr(self.report.report,"list")
        delattr(self.report.report,"result")
        
        if self.to_clean:
#             rmdir(self.apk_file+".png", True)
#             rmdir(self.apk_file+".resign.png", True)
#             rmdir(self.apk_file+".inforce.png", True)
            
            self.clean()        

if __name__=="__main__":
    AssTestInforce().main()