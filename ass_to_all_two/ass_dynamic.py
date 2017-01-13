# -*- coding:utf-8 -*-
import permission
from assbase import AssBase,Items,Report,AssEncoder

class AssDynamic(AssBase):
    #格式化检测信息，添加报告输出列表
    #[code 相关信息] [comment 问题描述] [result 等级] [name 检测说明] [method 检测方法]
    def addItem(self, code, comment='', result='高危', name='攻击检测', method='全自动化分析'):
        items = Items()
        items.checkMethod = self.i18n(method)
        items.checkName = self.i18n(name)
        items.checkResult = self.i18n(result)
        items.relatedCode = code
        items.resultComment = self.i18n(comment)

        self.report.list[0].items.append(items)
        self.addResultValue(self.i18n(result))

    #格式化信息，添加到临时列表
    #[arr 目标数组] [obj 信息]
    def addArr(self, arr, obj):
        if obj=='':
            return False
        else:
            arr.append(obj)
            return True
    
    #格式化信息，添加到输出报告列表
    #[arr 目标数组] [comment 信息]     
    def addArrItem(self, arr, comment):
        if len(arr)>0:
            self.addItem(','.join(arr), comment)
    
    #检测权限等级
    #[per 权限]
    def check_permission(self, per):
        comment = ''
        result = ''

        if per in permission.high_risk.keys():#高危风险权限
            result = '高危'
            comment = permission.high_risk[per]
        elif per in permission.medium_risk.keys():#危险风险权限
            result = '危险'
            comment = permission.medium_risk[per]
        elif per in permission.low_risk.keys():#普通风险权限
            result = '普通'
            comment = permission.low_risk[per]
        else:
            result = '其他'
        
        if result != '普通':
            self.addItem(per, comment, result, '权限检查')

    #获取app包信息
    def app_package_info(self):
        permission_begin = False
        permission_end = False
        
        self.report.basic.packageName = self.apk
        
        lines = self.drozer("run app.package.info -a "+self.apk)
        for line in lines:
            val = self.get_val(line, 'Application Label:')
            if val!='':
                self.report.basic.appName = val
     
            val = self.get_val(line, 'Version:')
            if val!='':
                self.report.basic.appVersion = val
     
            index = line.find('Uses Permissions:')
            if index>=0:
                permission_begin = True
                continue
     
            index = line.find('Defines Permissions:')
            if index>=0:
                permission_end = True
             
            if permission_begin and not permission_end:
                per = line.replace('-','').strip()
                if per == '':
                    break
                else:
                    self.check_permission(per)

    #获取app provider信息
    def app_provider_info(self):
        cp_arr = []
        
        lines = self.drozer("run app.provider.info -a "+self.apk)
        for line in lines:
            val = self.get_val(line, 'Content Provider:')
            self.addArr(cp_arr, val)
        
        return cp_arr
    #获取app 攻击面信息
    def app_package_attacksurface(self):
        attack_activities = ''
        attack_receivers = ''
        attack_providers = ''
        attack_services = ''
        attack_debuggable = False
        attacks = 0
         
        lines = self.drozer("run app.package.attacksurface "+self.apk)
        for line in lines:
            val = self.get_val(line, 'activities exported', False)
            if val != '':
                attack_activities = val
                attacks += int(val)
           
            val = self.get_val(line, 'broadcast receivers exported', False)
            if val != '':
                attack_receivers = val
                attacks += int(val)
               
            val = self.get_val(line, 'content providers exported', False)
            if val != '':
                attack_providers = val
                attacks += int(val)
        
            val = self.get_val(line, 'services exported', False)
            if val != '':
                attack_services = val
                attacks += int(val)
        
            index = line.find('is debuggable')
            if index>=0:
                attack_debuggable = True
    
        if attack_debuggable or attacks > 0:#判断应用存在可被调试风险
            comment = ''
                
            if attacks > 0:
                comment += attack_activities+' activities, '+attack_receivers+' broadcast receivers, '+\
                    attack_providers+' content providers, '+attack_services+' services  exported. '
            if attack_debuggable:
                comment += ' '+self.i18n('应用存在可被调试风险')
                
            self.addItem(str(attacks), comment)
 
    #获取app activity信息   
    def app_activity_info(self):
        act_begin = False
        act_arr = []

        act = self.get_launchable_activity()
        
        lines = self.drozer("run app.activity.info -a "+self.apk)
        for line in lines:
            if line.find("Package:")>=0:
                act_begin = True
                continue
            
            if act_begin and act != line.strip():
                if not self.addArr(act_arr, line.strip()):
                    break
       
        self.addArrItem(act_arr, '应用存在高风险未被授权外部调用风险。此类应用暴露的活动可以通过后台静默方式被激发启用产生暴露关键或隐私数据风险。')
        
        return act_arr

    #外部启动app的activity  [activity app的activity名] 
    def app_activity_start(self, activity):
        lines = self.drozer("run app.activity.start --component "+self.apk+" "+activity)
        for line in lines:
            val = self.get_val(line, "Unable")
            if val == '':
                return False
        return True

    #应用资源风险评估
    def scanner_provider_finduris(self):
        all_uris = []
        access_uris = []
        uri_begin = False
        
        lines = self.drozer("run scanner.provider.finduris -a "+self.apk)
        for line in lines:
            val = self.get_val(line, "to Query ")
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
       
        self.addArrItem(access_uris, "应用在系统中相关资源存在暴露和被未授权访问风险。第三方未授权应用、工具或服务可以通过暴露的资源位置信息获取该应用资源信息。")
        
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
            if line.find("Injection in Projection:")>=0:
                ip_begin = True
                continue
            
            if line.find("Injection in Selection:")>=0:
                is_begin = True
                continue
        
            if ip_begin and not is_begin:
                if line.find("No ")<0:
                    self.addArr(ip_arr, line.strip())
                continue

            if is_begin:
                if line.find("No ")<0:
                    self.addArr(is_arr, line.strip())
      
        self.addArrItem(ip_arr, "应用存在反射漏洞注入风险。通过数据库访问手段采用外部引用反射应用内部逻辑方式，可以通过该漏洞利用对应用进行注入操作，引发被非法监控或植入恶代行为。")
        self.addArrItem(is_arr, "应用存在选择漏洞注入风险。通过数据库访问手段采用非法查询方式，可以通过该漏洞利用对应用进行注入操作，引发被非法监控或植入恶代行为。")
            
        return ip_arr, is_arr
    #应用存在脆弱点风险检测
    def scanner_provider_traversal(self):
        vp_begin = False
        vp_arr = []
        
        lines = self.drozer("run scanner.provider.traversal -a "+self.apk)
        for line in lines:
            if line.find("Vulnerable Providers:")>=0:
                vp_begin = True
                continue
            
            if vp_begin:
                if line.find("No ")>=0:
                    break
                else:
                    self.addArr(vp_arr, line.strip())
        
        self.addArrItem(vp_arr, '应用存在脆弱点风险。提供内容中存在被利用漏洞风险。')
        return vp_arr
    #获取应用服务信息
    def app_service_info(self):
        s_begin = False
        s_arr = []
        
        lines = self.drozer("run app.service.info -a "+self.apk)
        for line in lines:
            if line.find("Package:"+self.apk)>=0:
                s_begin = True
                continue
            
            if s_begin:
                if line.find("No ")>=0:
                    break
                else:
                    self.addArr(s_arr, line.strip())

        self.addArrItem(s_arr, 'servies')
        return s_arr
    
    def run(self, apk_file):
        self.report = Report()
        self.set_apk(apk_file)
        self.progress_total = 12

        self.run_ass()
        
        self.updateResult()
        
        out_file = self.apk_file+".json";
        if len(self.language)>0:
            out_file += "."+self.language
        
        self.write_file(out_file, AssEncoder(indent=2,ensure_ascii=False).encode(self.report))
        
        self.progress("扫描完成", True)
        
        
    def run_ass(self):
        self.connect_adb()

        #安装apk文件
        ret = self.adb("install -r \""+self.apk_file+"\"")
        print(ret)
        if ret.find("Success")<0 and ret.find("INSTALL_FAILED_ALREADY_EXISTS")<0:
            print(self.i18n("安装失败"))
            return 1
        
        #获取apk package name
        self.progress("获取包名")
        apk = ''
        ret = self.get_package_info()
        lines = ret.splitlines()
        if len(lines)>0:
            apk = self.get_val(lines[0], "package: name='")
            apk = self.get_val(apk, "' version", False)
        
        if apk == '':
            print(self.i18n('无法获取包名'))
            return 2
    
        self.apk = apk    
        
        self.progress("获取包信息")
        self.app_package_info()
    
        self.progress("获取供应信息")
        self.app_provider_info()
     
        self.progress("检测攻击面")
        self.app_package_attacksurface()
     
        self.progress("获取activity信息")
        activities = self.app_activity_info()
     
        self.progress("启动activity")
#         for act in activities:
#             self.app_activity_start(act)
         
        self.progress("扫描非法uri")
        all_uri, access_uri = self.scanner_provider_finduris()
     
        self.progress("检测数据漏洞")
        for uri in all_uri:
            self.app_provider_query(uri)
            self.app_provider_read(uri)
            self.app_provider_download(uri)
        
        self.progress("扫描注入信息")
        self.scanner_provider_injection()
        
        self.progress("扫描数据")
        self.scanner_provider_traversal()
        
        self.progress("获取服务信息")
        self.app_service_info()
        
        print(self.adb("uninstall "+self.apk))


if __name__=="__main__":
    AssDynamic().main()
