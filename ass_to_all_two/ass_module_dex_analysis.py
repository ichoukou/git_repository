# -*- coding: utf-8 -*-

import sys
import os
import ass_base
from ass_module import AssModule
from androguard.core.androgen import AndroguardS
from androguard.core.analysis import analysis
from androguard.core.bytecodes.dvm import *
from ass_report import  AssReport


keyword_list = [#type:0:str  1:methodNoParam   2:methodParam
            {'id':'0_20', 'key1':['addJavascriptInterface'], 'class1':'Landroid/webkit/WebView', 'type':'1'},
            {'id':'1_5', 'key1':['password','passwd','passw','pass'], 'type':'0'},
            {'id':'1_6', 'key1':['key','def_keyword'], 'type':'0'},
            {'id':'1_9', 'key1':['const-string'], 'type':'0'},
            {'id':'1_10', 'key1':['getInstance'], 'class1':'Ljava/security/KeyFactory', 'param1':['RSA'], 'key2':['getInstance'], 'class2':'Ljava/security/MessageDigest', 'param2':['MD5','SHA-1','SHA-256','SHA-512'], 'key3':['getInstance'], 'class3':'Ljavax/crypto/Cipher', 'param3':['DES','AES'],'not':'1','type':'222'},
            {'id':'1_9', 'key1':['^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$'],'type':'0'},
            {'id':'2_3', 'key1':['(http|File)://[^\s]+\.[^\s]+'], 'type':'0'},
            {'id':'1_11', 'key1':'forName', 'class1':'Ljava/lang/Class', 'type':'1'},
            {'id':'0_6', 'key1':['v', 'i', 'd', 'e', 'w'], 'class1':'Landroid/util/Log', 'type':'1'},
            {'id':'1_12', 'key1':['insert into','update','delete from'], 'type':'0'},
            {'id':'1_8', 'key1':['exec'], 'class1':'Ljava/lang/Runtime', 'param1':['su'], 'type':'2'},
            {'id':'3_0', 'key1':['PhoneGlobals$NotificationBroadcastReceiver'], 'key2':['engineNextBytes'], 'class2':'Ljava/security/SecureRandomSpi', 'type':'01'},
            {'id':'1_0', 'key1':['GET_SIGNATURES'], 'key2':['getCrc'], 'class2':'Ljava/util/zip/ZipEntry', 'not':'1', 'type':'01'},
            {'id':'3_3', 'key1':['((https?)|ftp)://[^\s]+\.[^\s]+'], 'type':'0'},
            {'id':'3_13', 'key1': ['getName'], 'class1': 'Ljava/util/zip/ZipEntry', 'type':'1'},
            {'id':'0_22', 'key1':['registerReceiver'], 'class1':'Landroid/app/ApplicationContext', 'type':'1'},
            {'id':'0_23', 'key1':['isDebuggerConnected'], 'class1':'Landroid/os/Debug', 'type':'1'},
            {'id':'3_7', 'key1':['setHostnameVerifier'], 'class1':'Ljavax/net/ssl/HttpsURLConnection', 'param1':['SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER'], 'type':'2'},
            {'id':'1_23', 'key1':['setSeed'], 'class1':'Ljava/security/SecureRandom', 'key2':['SecureRandom'], 'class2':'Ljava/security/SecureRandom','type':'11'},
            {'id':'0_24', 'key1':['getSerializableExtra','getAction'], 'class1':'Landroid/content/Intent', 'type':'1'},
            {'id':'3_13', 'key1':['proceed'], 'class1':'Landroid/webkit/SslErrorHandler', 'type':'1'},
            {'id':'1_22', 'key1':['removeJavascriptInterface'], 'class1':'L', 'param1':['searchBoxJavaBridge_','accessibilityTraversal','accessibility'], 'not':'1', 'type':'2'}
            ]

class AssDexAnalysis(AssModule):
    def init(self, argv):
        super(AssDexAnalysis, self).init(argv)
        self.analysis_apk(self.apk_file)

    def analysis_apk(self, apkpath):#apk dex analysis
        self.a = AndroguardS(apkpath)
        self.x = analysis.VMAnalysis(self.a.get_vm())
        self.classes = self.a.get_vm().get_classes_names()


    def search_method_withparams(self, class_name, method_namelist, descriptor, param_list):#search a method that have params
        pathdic = {}
        for method_name in method_namelist:
            paths = analysis.get_Paths(self.a, self.x.get_tainted_packages().search_methods( class_name, method_name, descriptor))
            for path in paths:
                pathset = path['src'].split(' ', 2)
                method_class_set = self.a.get_vm().get_methods_class(pathset[0])
                for method in method_class_set:
                    if method.get_name() == pathset[1] and method.get_descriptor() == pathset[2]:
                        code = method.get_code()
                        if code == None:
                            continue
                        bc = code.get_bc()
                        instructions = [i for i in bc.get_instructions()]
                        for instruction in instructions:
                            if self.check_params(instruction, param_list):
                                pathdic[pathset[0][:-1]] = pathset[0][:-1] + "/" + pathset[1]
        return  pathdic.values()

    def check_params(self, instruction, param_list):#match the param
        if isinstance(instruction,Instruction21c) and instruction.get_op_value()==0x1A:
            outputset = instruction.get_output(-1)
            for listItem in param_list:
                if listItem in outputset:
                    return True
        return False

    def search_method_noparams(self, class_name, method_namelist, descriptor):#search a method that have no param
        pathdic = {}
        for method_name in method_namelist:
            #print "search method", package_name, method_name, descriptor
            #analysis.show_Paths(self.a, self.x.get_tainted_packages().search_methods( package_name, method_name, descriptor) )
            paths = analysis.get_Paths(self.a, self.x.get_tainted_packages().search_methods( class_name, method_name, descriptor))
            # for path in paths:
            #     pathset = path['src'].split(' ')
            #     if class_name == pathset[0][0:-1]:
            #         pathdic[pathset[0][:-1]] = pathset[0][:-1] + "/" + pathset[1]
            #     elif class_name == "all":
            #         pathdic[pathset[0][:-1]] = pathset[0][:-1] + "/" + pathset[1]
            #     else:
            #         continue
            for path in paths:
                pathset = path['src'].split(' ')
                pathdic[pathset[0][:-1]] = pathset[0][:-1] + "/" + pathset[1]
        return pathdic.values()


    def search_str(self,stringItem):#search all strings
        for s, _ in self.x.get_tainted_variables().get_strings():
            if stringItem == _:
                return s.get_paths()
        return None

    def match_str(self,keywordlist):#match the specific string
        strDict = {}
        for keyword in keywordlist:
            stringset = self.a.get_vm().get_regex_strings(keyword)
            for stringsetItem in stringset:
                pathInfo = self.search_str(stringsetItem)
                if pathInfo == None:
                    continue
                strDict[stringsetItem] = []
                for path in pathInfo:
                    access, idx = path[0]
                    m_idx = path[1]
                    method = self.a.get_vm().get_cm_method(m_idx)
                    strDict[stringsetItem].append("{:s}->{:s} {:s}".format(method[0], method[1], method[2][0] + method[2][1]))
        vadlist = []
        for va in strDict.values():
            vadlist.extend(va)
        return vadlist

    def run(self):
        print "dex analysis  begin"
        super(AssDexAnalysis, self).run()
        for keyworddict in keyword_list:
            print keyworddict['id']
            riskdic = {"strrisk":[], "methNoParam":[], "methWithParam":[]}
            n = 1
            for type in keyworddict['type']:
                pkey = 'key'
                pclass = 'class'
                pparam = 'param'
                if type == '0':
                    strkey  = keyworddict[ pkey + str(n) ]
                    riskdic["strrisk"].extend(self.match_str(strkey))
                    n = n + 1
                elif type == '1':
                    methnokey = keyworddict[ pkey + str(n) ]
                    methnoclass = keyworddict[ pclass + str(n) ]
                    riskdic["methNoParam"].extend(self.search_method_noparams(methnoclass, methnokey, "."))
                    n = n + 1
                else:
                    methwithkey = keyworddict[ pkey + str(n) ]
                    methwithclass = keyworddict[ pclass + str(n) ]
                    methwithparam = keyworddict[ pparam + str(n) ]
                    riskdic["methWithParam"].extend(self.search_method_withparams(methwithclass, methwithkey, ".", methwithparam))
                    n = n + 1
            flag = self.judge_rule(riskdic, "or" , keyworddict['type'])
            if keyworddict.has_key('not'):
                flag = not flag
            if flag:
                account,riskString = self.convertDictToStr(riskdic)
                #self.report.setItem(keyworddict['id'], self.convertDictToStr(riskdic))
                self.report.setItem(keyworddict['id'], riskString,account)
        print "dex analysis  end"

    def convertDictToStr(self, dict):
        num = 0
        Tostr = ""
        if dict["strrisk"] != None and len(dict["strrisk"]) != 0:
            for i in dict["strrisk"]:
                print "**************************************************"
                print type(i)
                Tostr += (i + "\n")
            num += len(dict["strrisk"])
            print num

        if dict["methNoParam"] != None and len(dict["methNoParam"]) != 0:
            for i in dict["methNoParam"]:
                print "**************************************************"
                print type(i)
                Tostr += (i + "\n")
            num += len(dict["methNoParam"])
            print num
        if dict["methWithParam"] != None and len(dict["methWithParam"]) != 0:
            for i in dict["methWithParam"]:
                print "**************************************************"
                print type(i)
                Tostr += (i + "\n")
            num += len(dict["methWithParam"])
            print num
        print num
        restr = "风险数量："+ str(num) + "\n" + Tostr
        return (num,restr)
        #return restr
        #return Tostr

    def judge_rule(self, dic , rule , type):
        b1 = b2 = b3 = 0
        if "0" in type:
            if dic.has_key("strrisk") and len(dic["strrisk"]) == 0 :
                b1 = -1 # no risk
            else:
                b1 = 1 #exist risk
        if "1" in type:
            if dic.has_key("methNoParam") and len(dic["methNoParam"]) == 0:
                b2 = -1
            else:
                b2 = 1
        if "2" in type:
            if dic.has_key("methWithParam") and len(dic["methWithParam"]) == 0:
                b3 = -1
            else:
                b3 = 1
        if rule == "or":
            return b1 > 0 or b2 > 0 or b3 > 0
