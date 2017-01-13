# -*- coding:utf-8 -*-
import permission
import ass_base
from ass_module import AssModule
import ass_report
import re,time
from os.path import join, getsize

class AssDynamic(AssModule):
    #格式添加到数组
    #[arr 需添加数组] [obj 信息]
    def addArr(self, arr, obj):
        if obj=='':
            return False
        else:
            arr.append(obj)
            return True
    #检测权限等级
    #[per 权限]
    def check_permission(self, per):#检查权限
        self.report.setPermissionItem('5_' + per, per)

    #获取app包信息
    def app_package_info(self):#获取包信息
        permission_begin = False
        permission_end = False
        
        #self.report.report.basic.packageName = self.apk
        print self.apk
        self.report.setBaseInfo(self.apk, 2)            #设置包名
        
        lines = self.drozer("run app.package.info -a "+self.apk)
        for line in lines:
            val = ass_base.get_val(line, 'Application Label:')
            print val
            if val != '':
                #self.report.report.basic.appName = val
                self.report.setBaseInfo(val, 0)         #设置应用名
     
            val = ass_base.get_val(line, 'Version:')
            print val
            if val != '':
                #self.report.report.basic.appVersion = val
                self.report.setBaseInfo(val, 1)         #设置版本号
     
            index = line.find('Uses Permissions:')
            if index >= 0:
                permission_begin = True
                continue
     
            index = line.find('Defines Permissions:')
            if index >= 0:
                permission_end = True
             
            if permission_begin and not permission_end:
                per = line.replace('-', '').strip()
                if per == '':
                    break
                else:
                    self.check_permission(per)

    #获取app provider信息
    def app_provider_info(self):#获取供应信息
        cp_arr = []
        
        lines = self.drozer("run app.provider.info -a " + self.apk)
        for line in lines:
            val = ass_base.get_val(line, 'Content Provider:')
            self.addArr(cp_arr, val)
        
        return cp_arr
    #获取app 攻击面信息
    def app_package_attacksurface(self):#获取攻击面信息
        attack_activities = ''
        attack_receivers = ''
        attack_providers = ''
        attack_services = ''
        attack_debuggable = False
        attacks = 0
         
        lines = self.drozer("run app.package.attacksurface " + self.apk)
        for line in lines:
            val = ass_base.get_val(line, 'activities exported', False)
            if val != '' and int(val) > 0:
                self.report.setItem('0_1', val + ' activities exported')
           
            val = ass_base.get_val(line, 'broadcast receivers exported', False)
            if val != '' and int(val) > 0:
                self.report.setItem('0_2', val + ' broadcast receivers exported')
               
            val = ass_base.get_val(line, 'content providers exported', False)
            if val != '' and int(val) > 0:
                self.report.setItem('0_4', val + ' content providers exported')
        
            val = ass_base.get_val(line, 'services exported', False)
            if val != '' and int(val) > 0:
                self.report.setItem('0_3', val + ' services exported')
        
            index = line.find('is debuggable')
            if index >= 0:
                self.report.setItem('0_0', 'android:debuggable=True')

    #获取app activity信息  
    def app_activity_info(self):#获取组件信息
        act_begin = False
        act_arr = []

        act = self.get_launchable_activity()
        
        lines = self.drozer("run app.activity.info -a " + self.apk)
        for line in lines:
            if line.find("Package:") >= 0:
                act_begin = True
                continue
            
            if act_begin and act != line.strip():
                if not self.addArr(act_arr, line.strip()):
                    break
       
        #self.report.addArrItem(act_arr, '应用存在高风险未被授权外部调用风险。此类应用暴露的活动可以通过后台静默方式被激发启用产生暴露关键或隐私数据风险。')
        
        return act_arr
    #外部启动app的activity  [activity app的activity名] 
    def app_activity_start(self, activity):#启动程序
        lines = self.drozer("run app.activity.start --component " + self.apk + " " + activity)
        for line in lines:
            val = ass_base.get_val(line, "Unable")
            if val == '':
                return False
        return True

    #三 应用资源风险评估
    def scanner_provider_finduris(self):
        all_uris = []
        access_uris = []
        uri_begin = False
        
        lines = self.drozer("run scanner.provider.finduris -a " + self.apk)
        for line in lines:
            val = ass_base.get_val(line, "to Query ")
            if val != '':
                try:
                    all_uris.index(val, )
                except ValueError:
                    all_uris.append(val)

                continue
            
            if line.find("Accessible content URIs:") >= 0:
                uri_begin = True
                continue
            
            if uri_begin:
                self.addArr(access_uris, line.strip())

        self.report.setItem('2-4', self.arrayToString(access_uris))
        #self.report.addArrItem(access_uris, '应用在系统中相关资源存在暴露和被未授权访问风险。第三方未授权应用、工具或服务可以通过暴露的资源位置信息获取该应用资源信息。')
        
        return all_uris, access_uris
    #请求uri [uri 应用内uri]
    def app_provider_query(self, uri):
        lines = self.drozer("run app.provider.query "+uri+" --projection \\\"'\\\"")
    #通过uri读取/etc/hosts [uri 应用内uri]       
    def app_provider_read(self, uri):
        lines = self.drozer("run app.provider.read "+uri+"/etc/hosts")
    #通过uri下载/etc/hosts [uri 应用内uri] 
    def app_provider_download(self, uri):
        lines = self.drozer("run app.provider.download "+uri+"/etc/hosts ./hosts")
        
    #四 应用注入风险评估  
    def scanner_provider_injection(self):
        ip_begin = False
        is_begin = False
        
        ip_arr = []
        is_arr = []
        
        lines = self.drozer("run scanner.provider.injection -a "+self.apk)
        for line in lines:
            if line.find("Injection in Projection:") >= 0:
                ip_begin = True
                continue
            
            if line.find("Injection in Selection:") >= 0:
                is_begin = True
                continue
        
            if ip_begin and not is_begin:
                if line.find("No ") < 0:
                    self.addArr(ip_arr, line.strip())
                continue

            if is_begin:
                if line.find("No ") < 0:
                    self.addArr(is_arr, line.strip())

        self.report.setItem('3-1', self.arrayToString(ip_arr))
        self.report.setItem('3-2', self.arrayToString(is_arr))
        #self.report.addArrItem(ip_arr, "应用存在反射漏洞注入风险。通过数据库访问手段采用外部引用反射应用内部逻辑方式，可以通过该漏洞利用对应用进行注入操作，引发被非法监控或植入恶代行为。")
        #self.report.addArrItem(is_arr, "应用存在选择漏洞注入风险。通过数据库访问手段采用非法查询方式，可以通过该漏洞利用对应用进行注入操作，引发被非法监控或植入恶代行为。")
            
        return ip_arr, is_arr
    #应用存在脆弱点风险检测
    def scanner_provider_traversal(self):
        vp_begin = False
        vp_arr = []
        
        lines = self.drozer("run scanner.provider.traversal -a " + self.apk)
        for line in lines:
            if line.find("Vulnerable Providers:") >= 0:
                vp_begin = True
                continue
            
            if vp_begin:
                if line.find("No ") >= 0:
                    break
                else:
                    self.addArr(vp_arr, line.strip())

        self.report.setItem('2-3', self.arrayToString(vp_arr))
        #self.report.addArrItem(vp_arr, '应用存在脆弱点风险。提供内容中存在被利用漏洞风险。')
        return vp_arr
#检查sqlite是否加密
    def app_sqlite_isEnc(self):#检查sqlite是否加密
        lines = self.adb("shell ls data/data/" + self.apk + "/databases")
        lines = lines.splitlines()
        dbfiles = []
        sql_arr = []

        dbSerach = re.compile(r'\.db$')
        encSerach = re.compile(r'encrypt') #如果加密 Error:file is encrypted or is not database
        for line in lines:
            if dbSerach.search(line):
                dbfiles.append(line)
        for dbfile in dbfiles:
            res = self.adb("shell sqlite3 /data/data/" + self.apk + "/databases/" + dbfile + " \".table\"")
            if not encSerach.search(res):
                self.addArr(sql_arr, dbfile.strip())
                self.addArr(sql_arr, res.strip())

        #self.report.addArrItem(sql_arr, '应用本地sqlite存储文件未加密处理')
        self.report.setItem('2-1', self.arrayToString(sql_arr))

    def app_service_info(self):#获取服务信息
        s_begin = False
        s_arr = []
        
        lines = self.drozer("run app.service.info -a " + self.apk)
        for line in lines:
            if line.find("Package:" + self.apk) >= 0:
                s_begin = True
                continue
            
            if s_begin:
                if line.find("No ") >= 0:
                    break
                else:
                    self.addArr(s_arr, line.strip())
        self.report.addArrItem(s_arr, 'servies')

        return s_arr
    
    def progress_total(self):
        return 12
        
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
        
        if apk == '':
            print(self.i18n('无法获取包名'))
            return 2

        self.report.progress("安装程序")
        self.apk = apk   
        self.connect_adb()
        self.adb("forward tcp:6001 tcp:31415")
        self.uninstall(apk)
        import chardet
        print chardet.detect(self.apk_file)
        if not self.install(self.apk_file):
            print 'install failde'
            return 1

        self.report.setBaseInfo(str(getsize(self.apk_file)/1024.0/1024.0) + 'M', 3)     #文件大小

        #启动程序完成必要初始化
        self.report.progress("启动程序")
        start_activity = self.get_launchable_activity()
        self.start_apk(apk, start_activity)

        #获取包信息
        self.report.progress("获取包信息")
        self.app_package_info()
        #获取供应信息
        self.report.progress("获取供应信息")
        self.app_provider_info()
        #检测攻击面
        self.report.progress("检测攻击面")
        self.app_package_attacksurface()
        #获取activity信息
        self.report.progress("获取activity信息")
        activities = self.app_activity_info()
        ##启动activity
        #   self.report.progress("启动activity")
        #   for act in activities:
        #       if act.find("Activity") >=0:
        #           self.app_activity_start(act)

         #扫描非法uri
        self.report.progress("扫描非法uri")
        all_uri, access_uri = self.scanner_provider_finduris()
        #检测数据漏洞
        #self.report.progress("检测数据漏洞")
        #for uri in all_uri:
            #self.app_provider_query(uri)
            #self.app_provider_read(uri)
            #self.app_provider_download(uri)
        #扫描注入信息
        self.report.progress("扫描注入信息")
        self.scanner_provider_injection()
        #扫描数据
        self.report.progress("扫描数据")
        self.scanner_provider_traversal()
        #获取服务信息
        #self.report.progress("获取服务信息")
        #self.app_service_info()
        
        #print(self.adb("uninstall "+self.apk))
        #获取进程PID，是否启动成功
        pid = self.get_pid(apk)
        if len(pid) != 0:
            #判断sqlite文件是否加密
            self.report.progress("获取sqlite信息")      
            self.app_sqlite_isEnc()


if __name__=="__main__":
    AssDynamic().main()
