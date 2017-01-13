#coding:utf8
import subprocess
import shutil
import os
import readConfig
import globalValues

globalValue = globalValues.globalValues()

def unpackApk (anprohelperPath, apkPath, folderPath):#解压

    if not(os.path.exists(anprohelperPath)):
        print ("\n Error, AnproHelper Not Found In: %s\n " %anprohelperPath)
        return 0

    if not(os.path.exists(apkPath)):
        print ("\n Error, APK Not Found In: %s\n " %apkPath)
        return 0

    if (os.path.exists(folderPath)):
        shutil.rmtree(folderPath)

    globalValue.ChangeToCmd()

    if globalValues.APKToolVersion == '2.0':
        command = 'java -jar "%s" d -f "%s" -o "%s" '%(anprohelperPath, apkPath, folderPath)
    else:
        command = 'java -jar "%s" d -f "%s" "%s" '%(anprohelperPath, apkPath, folderPath)

    print ("\n " + command + "\n ")

    shellcode =  subprocess.call(command, shell=True)

    if shellcode !=0:
        if globalValues.returnValue == 0:
            globalValues.returnValue = 2

    globalValue.BackToWork()

def repackApk (utilsPath, folderPath, outPutPath):#打包APK

    anprohelperPath = os.path.join(utilsPath, globalValues.APKToolsName)

    if not(os.path.exists(anprohelperPath)):
        print ("\n Error, AnproHelper Not Found In: %s\n " %anprohelperPath)
        return 0

    if not(os.path.exists(folderPath)):
        print ("\n Error, SourceFolder Not Found In: %s\n " %folderPath)
        return 0

    globalValue.ChangeToCmd()

    # pack apk
    if globalValues.APKToolVersion == '2.0':
        packCmd = 'java -jar "%s" b -f "%s" -o "%s" '%(anprohelperPath, folderPath, outPutPath)
    else:
        packCmd = 'java -jar "%s" b -f "%s" "%s" '%(anprohelperPath, folderPath, outPutPath)

    print ("\n " + packCmd + "\n ")

    shellcode = subprocess.call(packCmd, shell=True)
    if shellcode !=0:
        if globalValues.returnValue == 0:
            globalValues.returnValue = 3

    globalValue.BackToWork()

