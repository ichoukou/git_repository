# -*- coding:utf-8 -*-

import os
import ass_base
from ass_module import AssModule
import ass_config

#win



class AssCheckSo(AssModule):
    #判断so是否加密
    #[path so文件路径]
    def so_is_encrypt(self, path):#判断so是否加密
        out_str = self.do_cmd(ass_config.cmd_ndk_nm+" -D "+ass_base.q(path),False)
        java_func = ass_base.mid_str(out_str, " Java_", "\n")
        if len(java_func)>0 or out_str.find('android_log_print')>0:
            return -1
        elif out_str.find("JNI_OnLoad\n")>0:
            return 1
        else:
            return 0

    #获取未加密的so
    #[path so文件路径]     
    def get_unencrypt_so(self, toproot, topbegin, ext_name):#获取未加密的so
        topdir = os.path.join(toproot, topbegin)
        ext_len = len(ext_name)
        out_arr=[]
        for root, dirs, files in os.walk(topdir, topdown=False):
            #hanlde file
            for name in files:
                if name[-ext_len:] == ext_name:
                    path = os.path.join(root, name)
                    
                    if self.so_is_encrypt(path)<0:
                        disp_path = path.replace(toproot, '')
                        out_arr.append(disp_path)
        
        return out_arr
    
    def run(self):
        super(AssCheckSo, self).run()
        
        self.report.progress("检查so文件")
        #反编译apk文件
        self.smali(True)
        #获取未加密的so
        so_file = self.get_unencrypt_so(self.smali_dir, "lib", ".so")
        #self.report.addArrItem(so_file, 'so文件未加密', '源代码安全')

        #self.clean()
        
        if len(so_file)==0:
            return False

        self.connect_adb()
        apk,ver,label = self.get_package_base_info()
        start_activity = self.get_launchable_activity()
        #self.uninstall(apk)
        #self.install(self.apk_file)
        #self.start_apk(apk, start_activity)
        pid = self.get_pid(apk)
        if len(pid)==0:
        #    self.uninstall(apk)
            return False

       # self.adb("push tool/strace /data/")
        #self.adb("shell chmod 777 /data/strace")
        #使用strace工具挂载进程
        out_str = self.adb("shell /data/strace -p " + pid , 2)
        if out_str.find("Operation not permitted")>0:
            #self.uninstall(apk)
            return False
        #self.uninstall(apk)
        #self.report.addArrItem(so_file, 'so文件可被逆向调试', '源代码安全')
        self.report.setItem('0_0', self.arrayToString(so_file), True)
        
        
        
if __name__=="__main__":            
    AssCheckSo().main()   
