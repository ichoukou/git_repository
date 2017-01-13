# -*- coding:utf-8 -*-
'''

'''

import ass_config
import sys
from ass_base import b2u,u2b,mid_str,write_file
from ass_module import AssModule
import os

class AssDebug(AssModule):
    #检查资源xml [topdir 文件夹]
    def check_res_xml(self, topdir):#检查资源xml
        if os.path.exists(topdir):
            xmls = os.listdir(topdir)
            if len(xmls) > 0:
                xml = os.path.join(topdir, xmls[0])
                #使用工具编译资源xml文件
                out = self.do_cmd(ass_config.cmd_axml + " \"" + xml + "\"")
                if len(out) > 0:
                    #self.report.addItem(xmls[0]+":"+out[:200], '资源文件未加密处理', '源代码安全')
                    self.report.setItem('1_4', xmls[0] + ":" + out)
                    return True
        
        return False
    
    def progress_total(self):
        return 1
    
    def run(self):
        super(AssDebug, self).run()
        #检查源代码
        self.report.progress("检查源代码")
        
        apk, ver, label = self.get_package_base_info()
        start_activity = self.get_launchable_activity()
        
        #self.uninstall(apk)
        #self.install(self.apk_file)
        #self.adb("shell am start -e debug true "+apk+"/"+start_activity)

        #检查源代码信息
        self.smali(True)
        #检查资源xml
        self.check_res_xml(os.path.join(self.apk_file+".smali", 'res', 'layout'))
        
        manifest = self.get_manifest(apk)
        acts = self.get_all_activity(apk, manifest)
        if len(acts)>0:
            #self.report.addItem("AndroidManifest.xml:"+manifest[:200], '应用主配置文件未做安全处理', '源代码安全')
            self.report.setItem('1_7', "AndroidManifest.xml:" + manifest)
            
        pid = self.get_pid(apk)
        if len(pid) > 0:
            jdb_ini = ""

            #根据需求，调整调试样本总数
            for act in acts:
                jdb_ini += "stop in " + act + ".onCreate\n"
    #             jdb_ini += "class "+act+"\n"
    #         jdb_ini+="exit"
    #         jdb_ini += "run"
    #         jdb_ini+="trace method exits"
        
            write_file("jdb.ini", jdb_ini)
        
            self.adb("forward tcp:6002 jdwp:" + pid)
    #         self.do_cmd("\""+ass_config.cmd_jdb+"\" -connect com.sun.jdi.SocketAttach:hostname=localhost,port=6002")
            outstr = self.do_cmd(ass_config.cmd_jdb)
            #outstr = mid_str(u2b(b2u(outstr)), "设置断点", "\n") #中文返回
            outstr = mid_str(u2b(b2u(outstr)), "Deferring breakpoint", "\n") #英文返回
        
            if len(outstr) > 0:
                #self.report.addItem(outstr, "样本在运行过程中可被调试", "源代码安全")
                self.report.setItem('0_0', outstr, True)
            
        #self.clean()
        #卸载程序
        self.uninstall(apk)
         
        
if __name__=="__main__":
    if len(sys.argv)>1:            
        AssDebug().main()
    else:    
        AssDebug().do_cmd(ass_config.cmd_jdb)   
