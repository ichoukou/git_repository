# -*- coding:utf-8 -*-
import sys
import os
import ass_base
from ass_module import AssModule

#win

#黑代码
ad_text = '''
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    const-string v1, "\u8b66\u544a!\u8fd9\u91cc\u88ab\u9ed1\u4e86!"

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/AlertDialog;->show()V

'''

class AssTamper(AssModule):
    def run(self):
        super(AssTamper, self).run()
        try:
            #获取文件源码
            self.smali(True)
        
            apk = self.report.manager.getPackageName()
            start_activity = self.get_launchable_activity()
        
            #self.run_cap(apk, self.apk_file, start_activity, "org", True)
            #获取组件信息
            acts = self.get_all_activity(apk)
            for act in acts:
                self.crack_file(act, ad_text)
            #编译APK
            self.build_apk(self.apk_file+"_crack.apk")
            if os.path.exists(self.apk_file+"_crack.apk"):
                self.run_cap(apk, self.apk_file+"_crack.apk", start_activity, "crack")
                dir, filename = os.path.split(self.apk_file)
                #self.report.addItem(filename+'.org.png,' + filename + '.crack.png', '二次打包风险', '源代码安全')
                self.report.setItem('1_1', filename + '.apk, ' + filename + '_crack.apk')
        except:
            self.report.LOG_OUT("can not reback apk")

        self.clean()
        
if __name__=="__main__":            
    AssTamper().main()   
