#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import os.path
import time
import stat
from ass_module import AssModule
reload(sys)


class Apk:
    name = u"无"
    isVirus = False
    typeOfVirus = u"无"

    def __init__(self, name):
        self.name = name


#病毒检测
class VirusCheck(AssModule):

    #从一个文件路径复制到一个文件夹
    def copyFiles(self, sourceFile,  targetDir):

        filename = os.path.basename(sourceFile)
        targetFile = os.path.join(targetDir,  filename)
        #copy the files
        if os.path.isfile(sourceFile):
            open(targetFile, "wb").write(open(sourceFile, "rb").read())


    def run(self):
        sourceFile = self.apk_file
        targetDir = r'\\192.168.17.130\targetDir'
        filename = os.path.basename(sourceFile)

        apk = Apk(filename)

        self.copyFiles(sourceFile, targetDir)

        self.report.progress("病毒检测")

        fobj = open(os.path.join(targetDir, '1.txt'),'w')
        fobj.close()

        var = 1
        while var == 1:
            if os.path.isfile(os.path.join(targetDir, '2.txt')) == True:
                var = 0
                os.remove(os.path.join(targetDir, '2.txt'))

                time.sleep(5)

                targetFile = os.path.join(targetDir, filename)

                if os.path.isfile(targetFile) == False:
                    apk.isVirus = True
                    apk.typeOfVirus = "萌萌哒萌萌哒萌萌哒萌萌哒类型病毒"
                    self.report.setItem('4_1', apk.typeOfVirus + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')     #病毒检测结果
                else:
                    os.remove(targetFile)

        return apk
