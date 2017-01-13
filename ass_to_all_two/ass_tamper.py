#!/usr/bin/env python
#coding:utf8
import os
import sys
import shutil
import platform
import packunpack
import readConfig
import XMLParser
import fileOpt
import traceback
import globalValues
from optparse import OptionParser
from assbase import AssBase,Items,Report,AssEncoder
import subprocess

globalValue = globalValues.globalValues()

class APKTamper(AssBase):

    def start(self, inputFilePath, outputPath, fileName, config):

        currentDir = readConfig.getCurrentScriptPath()

        apkFilesPath = os.path.join(currentDir, config["apkFilesPath"])
        tempPath = os.path.join(currentDir, "tmp_"+ fileName)
        androidManifest = os.path.join(tempPath, "AndroidManifest.xml")
        utilsPath = os.path.join(currentDir, config["utilsPath"])
        filesPath = os.path.join(currentDir, config["filesPath"])
        apkPath = os.path.join(apkFilesPath, fileName)

        print ("\n APKPath: %s\n TmpPath: %s\n " %(apkPath, tempPath))

        if not(os.path.exists(apkFilesPath)):
            os.mkdir(apkFilesPath)

        # 判断APK是否已经保护过
        zipFile = os.path.join(utilsPath,'7za.exe')

        if not os.path.exists(zipFile):
            zipFile = '7za'

        assertLibPath = os.path.join(apkFilesPath, fileName[:-4])
        self.delete(assertLibPath)
        if self.sysstr == "Linux":
            cmd = 'unzip "%s" "lib/*" -d "%s"'%(apkPath, assertLibPath)
        else:
            cmd = ' %s x -aoa %s "assets" "lib"  -o%s '%(zipFile, apkPath, assertLibPath)
        subprocess.call(cmd, shell = True)
        #print ("\n command is %s\n" %cmd)
        #print ("\n Search path is: %s \n" %assertLibPath)

        for root,dirs,files in os.walk(assertLibPath):
            for temp in files:
                #print ("\n Search path is: %s \n" %temp)
                if temp.find(globalValues.IsBangBang) >= 0 or temp.find(globalValues.IsAjiami) >= 0 or temp.find(globalValues.IsProtect) >= 0 :
                    globalValues.returnValue = 1
                    delete(assertLibPath)
                    print ("This APK has been reinforced!!!")
                    sys.exit(1)

        self.delete(assertLibPath)

        # 解压APK
        packunpack.unpackApk(os.path.join(utilsPath, globalValues.APKToolsName), apkPath, tempPath)

        #读取values/String.xml和AndroidManifest.xml
        xmlparser = XMLParser.XMLParser(androidManifest, config)

        if len(globalValues.args) >= 2:
            #将args[1]保存到字典中
            if sysstr == "Linux":
                path_index = globalValues.args[1].rfind('/')+1
            else:
                path_index = globalValues.args[1].rfind('\\')+1
            out_path = globalValues.args[1][0:path_index]
            if (out_path[0] == '.'):
                out_path = sys.path[0]+out_path[1:]
            print ("out_path: %s" %out_path)
        else:
            out_path = outputPath

        #读string文件
        xmlparser.read_string_XML(tempPath)
        reader = xmlparser.get_XML_Result(out_path)

        #调用__init__函数
        file_opt = fileOpt.fileOpt(apkPath, filesPath, tempPath, outputPath)
        file_opt.set_reader(reader)
        file_opt.set_xmlparser(xmlparser)

        #file_opt.copySmaliFile()
        
    	#file_opt.copyLib()
        #新添加
        #file_opt.copyAssets()
        #file_opt.changeLauncher(androidManifest)
        #主activity文件onCreate中添加代码
        #file_opt.changeActivity()
        file_opt.addDialog()

        #重打包
        outPath = os.path.join(outputPath, fileName)
        file_opt.finish(outPath);
        print ('repackage App finish!')

    def delete(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

    def isApk(self, fileName):
        temp = fileName[-4:]
        if temp == '.apk':
            return True
        else:
            return False

    # 参数解析
    def parseArgs(self):

        self.AppTotal = 0
        self.AppSuccess = 0

        self.parser = OptionParser(usage = "usage:%prog [optinos] inputApkPath outputApkPath")

        self.parser.add_option("-v", "--version",
            action = "store_true",
            dest = "version",
            default = None,
            help = "print version number"
            )

        (options, args) = self.parser.parse_args()

        # 可扩展选项
        if options.version:
            print ("\nThe current version is: 0.1\n");

        globalValues.args = args

        if len(args) >= 1:      # 指定了apk路径
            print ("\n have appoint apk path\n ")

            try:
                # in linux: copy apk file from src path to  current-dir/apk
                fileName = args[0].split(os.sep)[-1]
                print ("--------------------------current App : %s--------------------------"%fileName)
                globalValues.returnValue = 0
                if not self.isApk(fileName):
                    return

                self.delete(os.path.join(self.inputPath, fileName))
                shutil.copy(args[0], os.path.join(self.inputPath, fileName))

                self.start(os.path.join(self.inputPath, fileName), self.outputPath, fileName, self.config)

                # copy out apk to destPath
                #outApk = os.path.join(outputPath, 'encyptOut', fileName.replace('.apk', '_d.apk'))
                outApk = os.path.join(self.outputPath, fileName)
                print ("outApk: %s" %outApk)
                if os.path.exists(outApk):
                    #shutil.copyfile(outApk, os.path.join(self.inputPath, ))
                    print ("--------------------------protect App : %s success!--------------------------\n"%fileName)
                else:
                    print ("\n ----------------------------------failed!-----------------------------------\n ")

                # 清理apk
                #self.delete(outApk)
                self.delete(os.path.join(self.inputPath,fileName))

            except:
                # 如果还没进行错误类型设定，则设置成未知错误
                if globalValues.returnValue == 0:
                    globalValues.returnValue = 6

                print ("--------------------------protect App : %s failed!--------------------------\n"%fileName)
                traceback.print_exc()

            print ("\n --------------------------------All finish!--------------------------------")
            print (" Error Code: %d\n "%globalValues.returnValue)
            sys.exit(globalValues.returnValue)

        # 使用默认路径 /src/apk
        else:
            for fileName in os.listdir(self.inputPath):
                if not self.isApk(fileName):
                    continue

                self.AppTotal = self.AppTotal + 1

                try:
                    print ("\n APKName: %s\n "%fileName)

                    print ("--------------------------current App : %s--------------------------"%fileName)
                    globalValues.returnValue = 0

                    self.start(os.path.join(self.inputPath, fileName), self.outputPath, fileName, self.config)
                    self.AppSuccess = self.AppSuccess + 1
                    print ("--------------------------protect App : %s success!--------------------------\n"%fileName)

                except:
                    print ("--------------------------protect App : %s failed!--------------------------\n"%fileName)

                    # 如果还没进行错误类型设定，则设置成未知错误
                    if globalValues.returnValue == 0:
                        globalValues.returnValue = 6

                    traceback.print_exc()

            print ("\n All finish, Total App Number: %d, Success App Number: %d, ErrCode: %d"%(self.AppTotal, self.AppSuccess, globalValues.returnValue))
            print ("############################################All finish!###########################################")
            sys.exit(globalValues.returnValue)

    def run(self, apk_file):
       print ("############################################start###########################################")

       self.sysstr = platform.system()
       self.rootDir = sys.path[0]
       self.config = readConfig.getConfig()
       self.inputPath = os.path.join(self.rootDir, self.config["apkFilesPath"])
       self.outputPath = os.path.join(self.rootDir, self.config["outFilesPath"])

       if(self.sysstr == "Windows"):
          print ("\n Works in Windows\n ")
          self.parseArgs()
       elif(self.sysstr == "Linux"):
          print ("\n Works in Linux\n ")
          self.parseArgs()

if __name__ == "__main__":
    APKTamper().main()
    

