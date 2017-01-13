# -*- coding:utf-8 -*-
import sys,os
import xml.dom.minidom

#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#判断当前平台
islinux = (sys.platform != "win32") 

#drozee 服务器连接地址
drozer_server = "127.0.0.1:6001"

#模拟器adb连接地址
# adb_server = "127.0.0.1:53001"
# adb_server = "127.0.0.1:5555"
adb_server = ""

cmd_jdb = None
cmd_aapt = None
cmd_anprohelper = None
cmd_drozer = None
cmd_adb = None
cmd_dex2jar = None
cmd_jar2java = None
cmd_sign = None
cmd_axml = None
cmd_7za = None
cmd_ndk_nm = None
cmd_ndk_gdb = None
pdf_template = None

dom = None
configXML = None
configRoot = None
itemList = None
pinggu_dir = None

if islinux:
    #打开xml文档
    dom = xml.dom.minidom.parse(cur_file_dir() + '/config_linux.xml')
    #得到文档元素对象
    configXML = {}
    configRoot = dom.documentElement
    itemList = configRoot.getElementsByTagName('data')
    for item in itemList:
        configXML.setdefault(item.getAttribute("key"), item.getAttribute("value"))

    #程序本身路径
    pinggu_dir = configXML['basedir']

    cmd_jdb = pinggu_dir+"/tool_linux/jdb.sh"
    #aapt命令
    cmd_aapt = pinggu_dir+"/tool_linux/aapt"

    #anprohelper命令全路�?
    cmd_anprohelper = pinggu_dir+"/tool_linux/anprohelper.sh"

    #将报告转为PDF格式
    cmd_convertReport = pinggu_dir+"/tool_linux/wang1.sh '/usr/lib/libreoffice/' "

    #drozer命令路径（因为需要切换）
    cmd_drozer = "drozer"

    #adb命令全路�?
    #cmd_adb = pinggu_dir+"/tool/adb"
    cmd_adb = "adb"
    #dex2jar命令全路�?
    cmd_dex2jar = pinggu_dir+"/tool_linux/dex2jar/d2j-dex2jar.sh"

    #jar2java命令全路�?
    cmd_jar2java = pinggu_dir+"/tool_linux/jd.sh"

    #sign
    cmd_sign = pinggu_dir+"/tool_linux/sign.sh"

    #axml
    cmd_axml = pinggu_dir+"/tool_linux/axml.sh"

    #7za
    cmd_7za = pinggu_dir+"/tool_linux/7za"

    #ndk-nm
    cmd_ndk_nm = pinggu_dir+"/tool_linux/arm-linux-androideabi-nm"

    #ndk-gdb
    #cmd_ndk_gdb = "cmd /c C:/adt-bundle-windows-x86-20131030/sdk/android-ndk-r10d/ndk-gdb-py.cmd --adb=\""+cmd_adb+"\" -s "+adb_server+" --verbose --start --force --project="

    cmd_ndk_gdb = "cmd /c "+ configXML['ndkdir'] +"ndk-gdb-py --adb=\""+cmd_adb+"\" -s "+adb_server+" --verbose --start --force --project="

    #pdf模板
    pdf_template = pinggu_dir+"/assets/template.pdf"
else:
    #打开xml文档
    dom = xml.dom.minidom.parse(cur_file_dir() + '/config_win.xml')
    #得到文档元素对象
    configXML = {}
    configRoot = dom.documentElement
    itemList = configRoot.getElementsByTagName('data')
    for item in itemList:
        configXML.setdefault(item.getAttribute("key"), item.getAttribute("value"))

    #程序本身路径
    pinggu_dir = configXML['basedir']

    cmd_jdb = pinggu_dir+"/tool_win/jdb.bat"
    #aapt命令
    cmd_aapt = pinggu_dir+"/tool_win/aapt.exe"
    #anprohelper命令全路�?
    cmd_anprohelper = pinggu_dir+"/tool_win/anprohelper.bat "

    cmd_convertReport = pinggu_dir+'/tool_win/wang1.bat "C:/Program Files (x86)/LibreOffice 5" '

    #drozer命令路径（因为需要切换）
    cmd_drozer = pinggu_dir+"/tool_win/drozer.bat"

    #adb命令全路�?
    cmd_adb = pinggu_dir+"/tool_win/adb.exe"

    #dex2jar命令全路�?
    cmd_dex2jar = pinggu_dir+"/tool_win/dex2jar.bat"

    #jar2java命令全路�?
    cmd_jar2java = pinggu_dir+"/tool_win/jd.bat"

    #sign
    cmd_sign = pinggu_dir+"/tool_win/sign.bat"

    #axml
    cmd_axml = pinggu_dir+"/tool_win/axml.bat"

    #7za
    cmd_7za = pinggu_dir+"/tool_win/7za.exe"

    #ndk-nm
    cmd_ndk_nm = pinggu_dir+"/tool_win/arm-linux-androideabi-nm.exe"

    #ndk-gdb
    #cmd_ndk_gdb = "cmd /c C:\\adt-bundle-windows-x86-20131030\\sdk\\android-ndk-r10d\\ndk-gdb-py.cmd --adb=\""+cmd_adb+"\" -s "+adb_server+" --verbose --start --force --project="

    cmd_ndk_gdb = "cmd /c " + configXML['ndkdir'] + "ndk-gdb-py.cmd --adb=\"" + cmd_adb + "\" -s " + adb_server + " --verbose --start --force --project="

    #pdf模板
    pdf_template = pinggu_dir+"/assets/template.pdf"
