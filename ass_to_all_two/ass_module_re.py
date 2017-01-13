# -*- coding:utf-8 -*-

'''

'''

import sys
import os
from ass_module import AssModule
import json
import re
from ass_base import read_file

def_keyword = [{'key':'password|passwd|passw|pwd|pass','name':'可能存在密码直接写在代码中，或者未使用专用密码输入法','cat':'源代码安全'},
           {'key':'key|keyword','name':'密钥直接写在代码里','cat':'源代码安全'},
           {'key':'const-string ','name':'硬编码字符串','cat':'源代码安全'},
           {'key':'RSAPublicKey|javax.crypto.Cipher|ENCRYPT\(|"MD5"|"RSA"|"SHA"|"MD2"|base64|DES','name':'没有使用加密算法','not':'1','cat':'源代码安全'},
           {'key':'\"1[3456789]\\d{9}\"','name':'手机号直接写在代码里','cat':'源代码安全'},
           {'key':'http://|File','name':'使用了不安全的网络协议','cat':'数据传输安全'},
           {'key':'forName','name':'应用了全反射机制','cat':'源代码安全'},
           {'key':"Log\.",'name':'含有调试信息','cat':'数据存储安全'},
           {'key':" insert into | update | delete from ",'name':'直接SQL语句','cat':'源代码安全'},
           {'key':"Runtime.getRuntime\(\).exec\(['\"]su['\"]\)",'name':'调用root权限','cat':'权限检查'},
           {'key':'com.android.phone.PhoneGlobals$NotificationBroadcastReceiver|engineNextBytes','name':'电话拨打权限绕过漏洞(CVE-2013-6272)','cat':'源代码安全'},
           {'key':'GET_SIGNATURES|getCrc\(\)|Signature|signatures','not':'1','name':'未对自身和系统签名信息进行必要的安全性检查','cat':'安全增强性测试'},
           {'key':'System.loadLibrary','name':'调用了so文件','cat':'源代码安全','condition':'has_so'}
           ]

class AssRe(AssModule):
    #从文件读取，设置检测关键词清单
    #[json_file 关键词清单]
    def set_keyword(self, json_file=''):#设置关键词
        if json_file != '':
            try:
#                 self.write_file("new.json", json.dumps(def_keyword))
                
                with open(json_file) as fp:
                    self.keyword = json.load(fp)
                print(type(self.keyword), self.keyword)
            except:
                print("error of load json")
                self.keyword = def_keyword
        else:
            self.keyword = def_keyword
            
    def init(self, argv):
        super(AssRe, self).init(argv)
        
        if len(argv)>4 and argv[4]!='-':
            self.set_keyword(argv[4])
        else:
            self.set_keyword()

        self.abc = []
        self.decompile = []
        self.condition = {}
        return True
    #建立源码索引
    #[writer 写入文件对象]
    def build_src_index(self, writer, ext):
        topdir = os.path.join(self.apk_file+"."+ext, ext)
        ext_name = "."+ext
        ext_len = len(ext_name)
        for root, dirs, files in os.walk(topdir, topdown=False):
            #hanlde file
            if root.find(os.path.join(topdir,"android"))==0:
                continue
            for name in files:
                if name[-ext_len:] == ext_name:
                    if len(name[:-ext_len])==1 and name[:-ext_len]!='R':
                        self.abc.append(name)
                    path = os.path.join(root,name)
                    disp_path = path.replace(topdir, '')
                    self.decompile.append(disp_path)
#                     print(path, self.read_file(path))
                    writer.append({'path':disp_path,'content':read_file(path)})
        
    def build_index(self, force=False):
        self.dex2jar(force)
        
#         self.smali(force)

        writer = []
        self.build_src_index(writer, "java")
        
        return writer
    
    def get_code_files(self):#获取文件源码
        out = ''
        if len(self.decompile)>10:
            out = ','.join(self.decompile[:10])
        else:
            out = ','.join(self.decompile)
        
        return out+',...' 
    ##搜索文件
    def search(self,ixs,reg):#搜索文件
        for ix in ixs:
            m = reg.search(ix['content'])
            if m:
#                 print(m.start(), m.end(), m.group(0))
                return ix['path'], ix['content'][m.start()-50:m.end()+50]
        return '',''
        
    def run(self):

        super(AssRe, self).run()
        #扫描关键点
        self.report.progress("扫描关键点")
        
        self.get_package_info()
        
        ixs = self.build_index(True)

        if len(self.decompile)>0:
            self.report.addItem(', '.join(self.decompile[:10])+',...', "能被反编译", '源代码安全')
            
            if len(self.abc) < 3:
                self.report.addItem(', '.join(self.decompile[:10])+',...', "没有采用代码混淆技术", '源代码安全')

            for k in self.keyword:
#                 print(k['key'])
                reg = re.compile(k['key'])
                
                path , content = self.search(ixs, reg)
                
                if k.get('condition') != None:
                    self.condition[k.get('condition')] = path
                else:
                    if k.get('not')=='1':
                        if content =='':
                            self.report.addItem("", k['name'])
                    else:
                        if len(content)>0:
                            self.report.addItem(path+"\n"+content, k['name'],k['cat'])
        if self.to_clean:
            self.clean()        

if __name__=="__main__":
    AssRe().main()