# -*- coding:utf-8 -*-

import os
import ass_base
import ass_report
import codecs
from ass_module import AssModule
from whoosh.highlight import Formatter,get_text
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.analysis import RegexAnalyzer
from whoosh.writing import AsyncWriter
from whoosh.writing import IndexingError
import json

#检测关键词清单
def_keyword = [{'id':'1_5', 'key':'password OR passwd OR passw OR pwd OR pass','name':'可能存在密码直接写在代码中，或者未使用专用密码输入法','cat':'源代码安全'},
           {'id':'1_6', 'key':'key or def_keyword','name':'密钥直接写在代码里','cat':'源代码安全'},
           {'id':'1_9', 'key':'const-string ','name':'硬编码字符串','cat':'源代码安全'},
           {'id':'1_10', 'key':'RSAPublicKey or javax.crypto.Cipher or ENCRYPT( or "MD5" or "RSA" or "SHA" or "MD2" or base64 or DES','name':'没有使用加密算法','not':'1','cat':'源代码安全'},
           {'id':'1_9', 'key':'[13000000000 TO 18999999999]','name':'可能存在手机号直接写在代码里','cat':'源代码安全'},
           {'id':'2_2', 'key':'http:// OR File','name':'使用了不安全的网络协议','cat':'数据传输安全'},
           {'id':'1_11', 'key':'forName','name':'应用了全反射机制','cat':'源代码安全'},
           {'id':'0_6', 'key':"'Log.'",'name':'含有调试信息','cat':'数据存储安全'},
           {'id':'1_12', 'key':"'insert into ' or 'update ' or delete from",'name':'可能存在直接SQL语句','cat':'源代码安全'},
           {'id':'1_8', 'key':"Runtime.getRuntime().exec(\"su\")",'name':'调用root权限','cat':'权限检查'},
           {'id':'3_0', 'key':'com.android.phone.PhoneGlobals$NotificationBroadcastReceiver OR engineNextBytes','name':'电话拨打权限绕过漏洞(CVE-2013-6272)','cat':'源代码安全'},
           {'id':'1_0', 'key':'PackageManager.GET_SIGNATURES or getCrc()','not':'1','name':'未对自身和系统签名信息进行必要的安全性检查','cat':'自身验证安全'},
           #{'key':'System.loadLibrary','name':'直接调用so文件','cat':'源代码安全','condition':'has_so'}
           ]

class AssFormatter(Formatter):
    """Puts square brackets around the matched terms.
    """

    def format_token(self, text, token, replace=False):
        # Use the get_text function to get the text corresponding to the
        # token
        tokentext = get_text(text, token, replace)

        # Return the text as you want it to appear in the highlighted
        # string
        return "%s(*)" % tokentext
    
class AssKeyword(AssModule):
    #从文件读取，设置检测关键词清单
    #[json_file 关键词清单]
    def set_keyword(self, json_file=''):
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
        super(AssKeyword, self).init(argv)
        self.apk_index = self.apk_file+".index"
        
        if len(argv)>3:
            self.set_keyword(argv[3])
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
                    try:
                        writer.add_document(path=ass_base.b2u(disp_path), content=ass_base.b2u(ass_base.read_file(path)))
                    except ValueError, Argument:
                          print "add_document error : ", Argument
#                     print(path, self.read_file(path))
                    
    
    #建立源码索引写入对象
    #[ix 写入文件对象]     
    def build_index_writer(self, ix):
        try:
            writer = AsyncWriter(ix)
            self.build_src_index(writer, "java")
            writer.commit()
        except IndexingError as ie:
            print ie.message + "index Error!!!"

    #建立索引
    def build_index(self, force=False):
        self.dex2jar(force)
        
#         self.smali(force)
        
        ass_base.rmdir(self.apk_index, force)
        #判断文件内容
        if not os.path.exists(self.apk_index):
            os.mkdir(self.apk_index)
            analyzer = RegexAnalyzer(ur"([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")
            schema = Schema(path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
            ix = create_in(self.apk_index, schema)
            self.build_index_writer(ix)
        else:
            ix = open_dir(self.apk_index)
        
        return ix

    #获取源码文件
    def get_code_files(self):
        out = ''
        if len(self.decompile)>10:
            out = ','.join(self.decompile[:10])
        else:
            out = ','.join(self.decompile)
        
        return out+',...' 
        
    def run(self):
        super(AssKeyword, self).run()
        #扫描关键点
        self.report.progress("扫描关键词点")
        
        ix = self.build_index(True)
        #检查关键信息
        if len(self.decompile)>0:
            #self.report.addItem(', '.join(self.decompile[:10])+',...', "能被反编译", '源代码安全')
            self.report.setItem('1_3', ', '.join(self.decompile) + ',...')
            
            if len(self.abc) < 3:
                #self.report.addItem(', '.join(self.decompile[:10])+',...', "没有采用代码混淆技术",  '源代码安全')
                self.report.setItem('1_2', ', '.join(self.decompile) + ',...')

            with ix.searcher() as searcher:
                for k in self.keyword:
                    query = QueryParser("content", ix.schema).parse(k['key'])
                    results = searcher.search(query, terms=True)
                    if len(results)>1 :
                        results.formatter = AssFormatter()
                        if k.get('condition') != None:
                            str = results[0]['path']
                            self.condition[k.get('condition')]=ass_base.u2b(str)
                        else:
                            if k.get('not')=='1':
                                if len(results)==0:
                                    #self.report.addItem("", k['name'])
                                    self.report.setItem(k['id'], u'无')
                            else:
                                if len(results)>0:
                                    #self.report.addItem(ass_base.u2b(results[0]['path']+"\n"+results[0].highlights("content")), k['name'], k['cat'])
                                    self.report.setItem(k['id'], ass_base.u2b(results[0]['path']+"\n"+results[0].highlights("content")))
        #print(self.condition.items())
    
        ix.close()
        self.clean()
        

if __name__=="__main__":
    AssKeyword().main()
