#coding:utf8
import os
import sys
import shutil
import platform

#全局变量
args = 'out'
returnValue = 0
sysstr = platform.system()
JavaHome = os.getenv('JAVA_HOME')
#WorkSpace = os.getcwd()
WorkSpace = sys.path[0]

#Python >= 2.6
#Java >= 1.70

#全局配置
APKToolsName = 'anprohelper.jar'
APKToolVersion = '2.0'
ManifestName = 'AndroidManifest.xml'
IsProtect = 'libcp.so'
IsBangBang = 'libsecexe.so'
IsAjiami = 'libexecmain.so'

class globalValues:

    def __init__(self):
        self.JavaHome = JavaHome

    def ChangeToCmd(self):
        #self.WorkSpace = os.getcwd()
        self.WorkSpace = sys.path[0]
        print ("\n >>> ChangeToCmd Before: %s"%self.WorkSpace)
        os.chdir(self.JavaHome)
        #print (" >>> ChangeToCmd After: %s\n"%os.getcwd())
        print (" >>> ChangeToCmd After: %s\n"%self.JavaHome)

    def BackToWork(self):
        #print ("\n <<< BackToWork Before: %s"%os.getcwd())
        print ("\n <<< BackToWork Before: %s"%self.JavaHome)
        os.chdir(self.WorkSpace)
        #self.WorkSpace = os.getcwd()
        self.WorkSpace = sys.path[0]
        print (" <<< BackToWork After: %s\n"%self.WorkSpace)

