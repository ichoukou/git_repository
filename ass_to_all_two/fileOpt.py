#coding:utf8

import os.path
import shutil
import readConfig
import subprocess
import platform
import packunpack
import XMLParser
import ConfigParser
import copy
import globalValues
import sys
import string

globalValue = globalValues.globalValues()
sysstr = platform.system()

class fileOpt:

    def __init__(self, apkPath, filesPath, tempPath, outputPath):
        self.apkPath = apkPath
        self.filesPath = filesPath
        self.tempPath = tempPath
        self.config = readConfig.getConfig()
        self.sourceBinaryPath = os.path.join(self.filesPath, self.config["binaryPath"])
        self.sourceBinaryV7Path = os.path.join(self.filesPath, self.config["binaryV7Path"])
        self.sourceSmaliPath = os.path.join(self.filesPath, "smali")
        self.sourceAssetsPath = os.path.join(self.filesPath, self.config['assets'])
        self.targetLibPath = os.path.join(self.tempPath, self.config["libPath"])
        self.sourceLibPath = os.path.join(self.filesPath, self.config["libPath"])
        self.targetBinaryPath = os.path.join(self.tempPath, self.config["binaryPath"])
        self.targetBinaryV7Path = os.path.join(self.tempPath, self.config["binaryV7Path"])
        self.targetSmaliPath = os.path.join(self.tempPath, "smali")
        self.targetAssetsPath = os.path.join(self.tempPath, "assets")
        self.smaliNewPath = ""
        self.outPutPath = outputPath
        self.sysstr = platform.system()
        self.reader = {}
        self.xmlparser = None

        self.libName = self.config["libName"]
        self.targetPath = tempPath
        self.targetResPath = os.path.join(self.targetPath, self.config["resPath"])

    def addDialog(self):
        print ("\n --------------addDialog to MainActivity--------------\n")
        activityPath = self.convertPath(self.reader['activityName'], 1) + ".smali"
        actSmaliPath = os.path.join(self.targetSmaliPath, activityPath)

        fp = open(actSmaliPath, "r")
        lines = fp.readlines()
        fp.close()
        i = 0
        addDiag2onCreate = []
        addDiag2onCreate.append('    new-instance v0, Landroid/app/AlertDialog$Builder;\n')
        addDiag2onCreate.append('    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V\n')
        addDiag2onCreate.append('    const-string v1, "ATTENTION!!!!"\n')
        addDiag2onCreate.append('    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;\n')
        addDiag2onCreate.append('    move-result-object v0\n')
        addDiag2onCreate.append('    const-string v1, "THIS APP IS HACKED!!!"\n')
        addDiag2onCreate.append('    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;\n')
        addDiag2onCreate.append('    move-result-object v0\n')
        addDiag2onCreate.append('    const-string v1, "OK"\n')
        addDiag2onCreate.append('    const/4 v2, 0x0\n')
        addDiag2onCreate.append('    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;\n')
        addDiag2onCreate.append('    move-result-object v0\n')
        addDiag2onCreate.append('    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;\n')
        addDiag2onCreate.append('\n')
        
        bFindPrologue = False
        bFindOnCreate = False
        bInAnnotation = False
        invoke = addDiag2onCreate
        count = 0
        i=0
        for line in lines:
            if (bFindOnCreate == False):
                if ((line.find("onCreate(") >= 0) and (line.find(".method") >= 0)):
                    bFindOnCreate = True
            else:
                if (line.find(".locals ") >= 0):
                    count = line.strip()[8:]
                    count1 = string.atoi(count)
                    if (count1 < 3):
                        lines[i] = line.replace(str(count1), "3")
                        print lines[i]
                    
                invoke = addDiag2onCreate
                if (line.find(".annotation") >= 0):
                    bInAnnotation = True

                if (line.find(".end annotation") >= 0):
                    bInAnnotation = False

                if (line.find(".prologue") >= 0):
                    bFindPrologue = True
					
                if (bFindPrologue == True and bInAnnotation == False):
                    # 定位到第一个不以'.'开头的非空字符串
                    if (line.strip() != '' and line.strip()[0] != '.'):
                        k = 0
                        for data in invoke:
                            lines.insert(i+k, data)
                            k = k + 1
                        bFindPrologue = True
                        break

                if (line.find(".end") >= 0) and (line.find("method") >= 0):
                    break
            i = i + 1

        #如果没有找到.prologue
        if (bFindPrologue == False):
            print ("\nnot find Prologue\n")
            i = 0
            bFindOnCreate = False
            for line in lines:
                if (bFindOnCreate == False):
                    if ((line.find("onCreate(") >= 0) and (line.find(".method") >= 0)):
                        bFindOnCreate = True
                else:
                    if (line.find(".locals") >= 0):
                        count = line.strip()[8:]
                        count1 = string.atoi(count)
                        if (count1 < 3):
                            lines[i] = line.replace(str(count1), "3")
                            print line[i]
                    
                    invoke = addDiag2onCreate
                    # 定位到第一个不以'.'开头的非空字符串
                    if (line.strip() != '' and line.strip()[0] != '.'):
                        k = 0
                        for data in invoke:
                            lines.insert(i+k, data)
                            k = k + 1
                        break

                    if (line.find(".end") >= 0) and (line.find("method") >= 0):
                        break
                i = i + 1

       
        #保存文件
        fp = open(actSmaliPath, "w")
        fp.writelines(lines)
        fp.close()
		
    def changeActivity(self): #修改调用组件
        print ("\n --------------changeActivity--------------\n")

        activityPath = self.convertPath(self.reader['activityName'], 1) + ".smali"
        actSmaliPath = os.path.join(self.targetSmaliPath, activityPath)

        fp = open(actSmaliPath, "r")
        lines = fp.readlines()
        fp.close()
        i = 0

        onCreateVerify = []
        onCreateVerify.append('.method public runVerify()V\n')
        onCreateVerify.append('    .locals 4\n')

        onCreateVerify.append('    .prologue\n')
        onCreateVerify.append('    :try_start_0\n')

        tmpCodeVefy = '    invoke-virtual {p0}, Lcom/example/MainActivity;->getCallingPackage()Ljava/lang/String;\n'
        tmpCodeVefy = tmpCodeVefy.replace('com/example/MainActivity', self.convertPath(self.reader['activityName'], 2))
        onCreateVerify.append(tmpCodeVefy)

        onCreateVerify.append('    move-result-object v0\n')
        onCreateVerify.append('    new-instance v1, Lcom/coral/sandbox/jni/VerifyIdentity;\n')
        onCreateVerify.append('    invoke-direct {v1}, Lcom/coral/sandbox/jni/VerifyIdentity;-><init>()V\n')
        onCreateVerify.append('    invoke-virtual {v1, p0, v0}, Lcom/coral/sandbox/jni/VerifyIdentity;->verify(Landroid/content/Context;Ljava/lang/String;)I\n')

        onCreateVerify.append('    move-result v0\n')
        onCreateVerify.append('    if-eqz v0, :cond_0\n')
        onCreateVerify.append('    const-string v0, "runVerify"\n')
        onCreateVerify.append('    const-string v1, "Verify Failed."\n')
        onCreateVerify.append('    invoke-static {v0, v1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I\n')
        onCreateVerify.append('    invoke-static {}, Lcom/coral/sandbox/jni/H;->getInstance()Lcom/coral/sandbox/jni/H;\n')
        onCreateVerify.append('    move-result-object v0\n')
        onCreateVerify.append('    invoke-virtual {v0}, Lcom/coral/sandbox/jni/H;->stopApp()I\n')
        onCreateVerify.append('    :try_end_0\n')
        onCreateVerify.append('    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0\n')
        onCreateVerify.append('    :cond_0\n')
        onCreateVerify.append('    :goto_0\n')
        onCreateVerify.append('    return-void\n')
        onCreateVerify.append('    :catch_0\n')
        onCreateVerify.append('    move-exception v0\n')
        onCreateVerify.append('    const-string v1, "runVerify"\n')
        onCreateVerify.append('    new-instance v2, Ljava/lang/StringBuilder;\n')
        onCreateVerify.append('    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V\n')
        onCreateVerify.append('    const-string v3, "#########catch"\n')
        onCreateVerify.append('    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n')
        onCreateVerify.append('    move-result-object v2\n')
        onCreateVerify.append('    invoke-virtual {v0}, Ljava/lang/Exception;->toString()Ljava/lang/String;\n')
        onCreateVerify.append('    move-result-object v0\n')
        onCreateVerify.append('    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n')
        onCreateVerify.append('    move-result-object v0\n')
        onCreateVerify.append('    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;\n')
        onCreateVerify.append('    move-result-object v0\n')
        onCreateVerify.append('    invoke-static {v1, v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I\n')
        onCreateVerify.append('    goto :goto_0\n')
        onCreateVerify.append('.end method\n')

        invokecode = []
        tmpcode = '    invoke-virtual {p0}, Lcom/example/MainActivity;->runVerify()V\n'
        tmpcode = tmpcode.replace('com/example/MainActivity', self.convertPath(self.reader['activityName'], 2))
        invokecode.append(tmpcode)

        invokecode2 = []
        invokecode2.append('    move-object/from16 v3, p0\n')
        tmpcode = '    invoke-virtual {v3}, Lcom/example/MainActivity;->runVerify()V\n'
        tmpcode = tmpcode.replace('com/example/MainActivity', self.convertPath(self.reader['activityName'], 2))
        invokecode2.append(tmpcode)

        bFindPrologue = False
        bFindOnCreate = False
        bInAnnotation = False
        invoke = invokecode
        count = 0

        for line in lines:
            if (bFindOnCreate == False):
                if ((line.find("onCreate(") >= 0) and (line.find(".method") >= 0)):
                    bFindOnCreate = True
            else:
                if (line.find(".locals ") >= 0):
                    count = line.strip()[8:]
                    print count
                    if (count > 16):
                        invoke = invokecode2
                    else:
                        invoke = invokecode

                if (line.find(".annotation") >= 0):
                    bInAnnotation = True

                if (line.find(".end annotation") >= 0):
                    bInAnnotation = False

                if (line.find(".prologue") >= 0):
                    bFindPrologue = True

                if (bFindPrologue == True and bInAnnotation == False):
                    # 定位到第一个不以'.'开头的非空字符串
                    if (line.strip() != '' and line.strip()[0] != '.'):
                        k = 0
                        for data in invoke:
                            lines.insert(i+k, data)
                            k = k + 1
                        bFindPrologue = True
                        break

                if (line.find(".end") >= 0) and (line.find("method") >= 0):
                    break
            i = i + 1

        #如果没有找到.prologue
        if (bFindPrologue == False):
            print ("\nnot find Prologue\n")
            i = 0
            bFindOnCreate = False
            for line in lines:
                if (bFindOnCreate == False):
                    if ((line.find("onCreate(") >= 0) and (line.find(".method") >= 0)):
                        bFindOnCreate = True
                else:
                    if (line.find(".locals") >= 0):
                        count = line.strip()[8:]
                        count1 = string.atoi(count)
                        if (count1 > 16):
                            invoke = invokecode2
                        else:
                            invoke = invokecode

                    if (line.find(".annotation") >= 0):
                        bInAnnotation = True

                    if (line.find(".end annotation") >= 0):
                        bInAnnotation = False
                    # 定位到第一个不以'.'开头的非空字符串
                    if (bInAnnotation == False and line.strip() != '' and line.strip()[0] != '.'):
                        k = 0
                        for data in invoke:
                            lines.insert(i+k, data)
                            k = k + 1
                        break

                    if (line.find(".end") >= 0) and (line.find("method") >= 0):
                        break
                i = i + 1

        # 在文件的最后面插入runVerify函数
        lens = len(lines)
        j = 1
        if (bFindOnCreate == True):
            for data in onCreateVerify:
                lines.insert(lens+j, data)
                j = j + 1
        else:
            for data in onCreateCode:
                lines.insert(lens+j, data)
                j = j + 1

        # 插个空字符，作为文件的EOF
        lines.insert(lens+j,'')

        #保存文件
        fp = open(actSmaliPath, "w")
        fp.writelines(lines)
        fp.close()

    def changeLauncher(self, targetAndroidManifestPath):

        print ("\n --------------changeLauncher--------------\n")

        fp = open(targetAndroidManifestPath, "r")
        lines = fp.readlines()
        fp.close()
        i = 0
        bFindCategory = False
        bFindApplication = False

        #添加权限
        permissionCode = []
        permissionCode.append('    <uses-permission android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS" />\n')
        permissionCode.append('    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />\n')
        permissionCode.append('    <uses-permission android:name="android.permission.READ_PHONE_STATE" />\n')
        #permissionCode.append('    <uses-permission android:name="android.permission.CHANGE_NETWORK_STATE" />\n')
        #permissionCode.append('    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />\n')
        #permissionCode.append('    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />\n')
        permissionCode.append('    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\n')
        permissionCode.append('    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />\n')
        permissionCode.append('    <uses-permission android:name="android.permission.INTERNET" />\n')

        #添加service
        serviceCode = []
        serviceCode.append('    <service android:name="com.coral.sandbox.service.HookService" >\n')
        serviceCode.append('    <intent-filter>\n')
        tmpCode = '        <action android:name="com.mam.sandboxservice.IHookServiceInterface" />\n'
        tmpCode = tmpCode.replace('com.mam.sandboxservice', self.reader['package_name'])
        serviceCode.append(tmpCode)
        serviceCode.append('        <category android:name="android.intent.category.DEFAULT" />\n')
        serviceCode.append('    </intent-filter>\n')
        serviceCode.append('    </service>\n')

        serviceCode.append('</application>\n')

        k = 0
        for line in lines:

            input_shortcut = "com.android.launcher.permission.INSTALL_SHORTCUT"
            output_shortcut = "com.android.launcher.permission.UNINSTALL_SHORTCUT"
            if (line.find(input_shortcut) >= 0):
                lines[i] = line.replace(input_shortcut, output_shortcut)

            if (bFindCategory == False):
                if (line.find("category") >= 0) and (line.find("android:name") >= 0):
                    input = "android.intent.category.LAUNCHER"
                    if (line.find(input) >= 0):
                        output = "android.intent.category.sandbox_LAUNCHER"
                        lines[i] = line.replace(input, output)
                        #lines.insert(i, line.replace(input, output))
                        bFindCategory = True

            if (bFindApplication == False):
                if  (line.find("</application>") >= 0):
                    input = "</application>"
                    output = "\n"
                    lines[i] = line.replace(input, output)
                    for data in serviceCode:
                        lines.insert(i+k, data)
                        k = k + 1
                    for data in permissionCode:
                        lines.insert(i+k, data)
                        k = k + 1
                    #line[i] = line.replace(input, serviceCode)
                    bFindApplication = True

            if ((bFindCategory == True) and (bFindApplication == True)):
                break

            i = i + 1

        if (bFindCategory == False):
            print ("\n The Application don't have Category\n")
            sys.exit(1);

        #保存文件
        fp = open(targetAndroidManifestPath, "w")
        fp.writelines(lines)
        fp.close()

    def addApplication(self, targetAndroidManifestPath):

        print ("\n --------------addApplication--------------\n")

        fp = open(targetAndroidManifestPath, "r")
        lines = fp.readlines()
        fp.close()
        i = 0
        bFindApplication = False

        for line in lines:
            if (bFindApplication == False):
                if (line.find("application") >= 0):
                    input = "application"
                    output = 'application android:name="com.coral.sandbox.jni.App"'
                    lines[i] = line.replace(input, output)
                    bFindApplication = True
                    break

            i = i + 1

        if (bFindApplication == False):
            print ("\n Not find Application\n")
            sys.exit(1);

        #保存文件
        fp = open(targetAndroidManifestPath, "w")
        fp.writelines(lines)
        fp.close()

    def insertCodeToApplication(self, targetSmaliPath, applicationName):

        print ("\n --------------insertCode 2 Application--------------\n")

        runHOnce = []
        runHOnce.append('.method public runHOnce()V\n')
        runHOnce.append('    .locals 1\n')
        runHOnce.append('    .prologue\n')
        tmpCode = '    invoke-virtual {p0}, Lcom/example/helloSandbox/HelloJni;->getApplicationContext()Landroid/content/Context;\n'
        tmpCode = tmpCode.replace('com/example/helloSandbox/HelloJni', self.convertPath(applicationName, 2))
        runHOnce.append(tmpCode)
        runHOnce.append('    move-result-object v0\n')
        runHOnce.append('    invoke-static {v0}, Lcom/coral/sandbox/jni/H;->runOnce(Landroid/content/Context;)Lcom/coral/sandbox/jni/H;\n')
        runHOnce.append('    return-void\n')
        runHOnce.append('.end method\n')

        invokecode = '    invoke-virtual {p0}, Lcom/example/helloSandbox/HelloJni;->runHOnce()V\n'
        invokecode = invokecode.replace('com/example/helloSandbox/HelloJni', self.convertPath(applicationName, 2))

        onCreateCode = []
        onCreateCode.append("# virtual methods\n")
        onCreateCode.append(".method public onCreate()V\n")
        onCreateCode.append("    .locals 1\n")
        onCreateCode.append("    .prologue\n")
        onCreateCode.append("    .line 13\n")
        onCreateCode.append("    invoke-virtual {p0}, Lcom/coral/sandbox/jni/App;->getApplicationContext()Landroid/content/Context;\n")
        onCreateCode.append("    move-result-object v0\n")
        onCreateCode.append("    invoke-static {v0}, Lcom/coral/sandbox/jni/H;->runOnce(Landroid/content/Context;)Lcom/coral/sandbox/jni/H;\n")
        onCreateCode.append("    .line 14\n")
        onCreateCode.append("    invoke-super {p0}, Landroid/app/Application;->onCreate()V\n")
        onCreateCode.append("    .line 15\n")
        onCreateCode.append("    return-void\n")
        onCreateCode.append(".end method\n")

        # copy 到 原包的applicationName中
        fileName = self.convertPath(applicationName, 1) + ".smali"

        appSmaliPath = os.path.join(targetSmaliPath, fileName)

        print ("appSmaliPath: %s\n" %appSmaliPath)

        fp = open(appSmaliPath, "r")
        appSmaliLines = fp.readlines()
        fp.close()
        i = 0
        bFindOnCreate = False
        bFindPrologue = False
        bInAnnotation = False

        for appSmaliLine in appSmaliLines:
            if (bFindOnCreate == False):
                if (appSmaliLine.find(".method public onCreate()V") >= 0):
                    bFindOnCreate = True
            else:
                if (appSmaliLine.find(".annotation") >= 0):
                    bInAnnotation = True

                if (appSmaliLine.find(".end annotation") >= 0):
                    bInAnnotation = False

                if (bFindPrologue == False and bInAnnotation == False):
                    # 定位到第一个不以'.'开头的非空字符串
                    if (appSmaliLine.strip() != '' and appSmaliLine.strip()[0] != '.'):
                        appSmaliLines.insert(i, invokecode)
                        bFindPrologue = True
                        break
                    if (appSmaliLine.find(".end") >= 0) and (appSmaliLine.find("method") >= 0):
                        break;

            i = i + 1

        # 在文件的最后面插入runHOnce函数
        lens = len(appSmaliLines)
        j = 1
        if (bFindOnCreate == True):
            for data in runHOnce:
                appSmaliLines.insert(lens+j, data)
                j = j + 1
        else:
            for data in onCreateCode:
                appSmaliLines.insert(lens+j, data)
                j = j + 1

        # 插个空字符，作为文件的EOF
        appSmaliLines.insert(lens+j,'')

        #保存文件
        fp = open(appSmaliPath, "w")
        fp.writelines(appSmaliLines)
        fp.close()


    #convert path
    def convertPath(self, inputName, convert_type):

        outputName = inputName

        if convert_type == 1:
        #包名转化为路径
            if(self.sysstr == "Windows"):
                outputName = inputName.replace(".", "\\")
            else:
                outputName = inputName.replace(".", "/")

        if convert_type == 2:
        #包名转化为smali里的路径
            outputName = inputName.replace(".", "/")

        if convert_type == 3:
        #路径转化为smali路径
            if(self.sysstr == "Windows"):
                outputName = inputName.replace("\\", "/")

        if convert_type == 4:
        #smali路径转化为路径
            if(self.sysstr == "Windows"):
                outputName = inputName.replace("/", "\\")

        if convert_type == 5:
            #smali路径转化为包名
            outputName = inputName.replace("/",".")

        return outputName


    def set_reader(self,reader):
        self.reader = reader

    def set_xmlparser(self,xmlparser):
        self.xmlparser = xmlparser


    #清除数据目录
    def doClean(self):
        shutil.rmtree(self.tempPath)

    #repackage
    def doZip(self, fileName):
        print ("\n --------------fileOpt doZip--------------\n")

        if not os.path.exists(self.outPutPath):
            os.makedirs(self.outPutPath)

        currentDir = readConfig.getCurrentScriptPath()
        utilsPath = os.path.join(currentDir, self.config["utilsPath"])
        packunpack.repackApk(utilsPath, self.tempPath, os.path.join(self.outPutPath, fileName).encode('utf8'))

    #重打包
    def finish(self, fileName):
        self.doZip(fileName)
        self.doClean()


    #循环遍历目录拷贝
    def getfilelist(self, sourcePath, targetPath):
        filelist = os.listdir(sourcePath)
        #修改soucePath  targetPath
        if sysstr == "Linux":
            for num in range(len(filelist)):
                filename = filelist[num]
                print ("copy filename: %s" %sourcePath+"/"+filename)
                if os.path.isdir(sourcePath+"/"+filename):
                    if os.path.exists(targetPath+"/"+filename):
                        self.getfilelist(sourcePath+"/"+filename, targetPath+"/"+filename)
                    else:
                        shutil.copytree(sourcePath+"/"+filename, targetPath+"/"+filename)
                else:
                    shutil.copy(os.path.join(sourcePath, filename), os.path.join(targetPath, filename))
        else:
            for num in range(len(filelist)):
                filename = filelist[num]
                print ("copy filename: %s" %sourcePath+"\\"+filename)
                if os.path.isdir(sourcePath+"\\"+filename):
                    if os.path.exists(targetPath+"\\"+filename):
                        self.getfilelist(sourcePath+"\\"+filename, targetPath+"\\"+filename)
                    else:
                        shutil.copytree(sourcePath+"\\"+filename, targetPath+"\\"+filename)
                else:
                    shutil.copy(os.path.join(sourcePath, filename), os.path.join(targetPath, filename))

    def copySmaliFile(self):
        print ("\n --------------fileOpt Copying SmaliFile--------------\n")

        #sourcePath = os.path.join(self.sourceSmaliPath, self.config["dexUtil"])
        #targetPath =  os.path.join(self.targetSmaliPath, self.config["dexUtil"])
        sourcePath = self.sourceSmaliPath
        targetPath = self.targetSmaliPath

        self.getfilelist(sourcePath, targetPath)

        # 原包没有application时候暂不修改
        if  self.reader['application'].strip() :
            self.insertCodeToApplication(self.targetSmaliPath, self.reader['application'])
        else:
            targetAndroidManifestPath = os.path.join(self.tempPath, "AndroidManifest.xml")
            self.addApplication(targetAndroidManifestPath)


    #复制assets
    def copyAssets(self):
        print ("\n --------------fileOpt Copying Assets File --------------\n")
        if not os.path.exists(self.targetAssetsPath):
            os.makedirs(self.targetAssetsPath)

        self.getfilelist(self.sourceAssetsPath, self.targetAssetsPath)

    #复制核心so库
    def copyLib(self):
        print ("\n --------------fileOpt Copying Native File --------------\n")

        #原包无lib，直接新建lib目录后copy
        if not os.path.exists(self.targetLibPath):
            #os.makedirs(self.targetBinaryPath)
            #sourcePath =  os.path.join(self.sourceBinaryPath, globalValues.IsProtect)
            #targetPath = os.path.join(self.targetBinaryPath, globalValues.IsProtect)
            #print ("\n Copying lib: %s <--> %s\n" %(sourcePath, targetPath))
            #shutil.copy(sourcePath, targetPath)
            #print ("\n Binary file Copy Succed ...\n ")
            shutil.copytree(self.sourceLibPath, self.targetLibPath)
            return
        #原包有armeabi目录
        if os.path.exists(self.targetBinaryPath):
            #sourcePath =  os.path.join(self.sourceBinaryPath, globalValues.IsProtect)
            #targetPath = os.path.join(self.targetBinaryPath, globalValues.IsProtect)
            sourcePath =  self.sourceBinaryPath
            targetPath = self.targetBinaryPath
            for item in os.listdir(sourcePath):
                shutil.copy(os.path.join(sourcePath, item), os.path.join(targetPath, item))
                print ("\n Copying lib: %s <--> %s\n "%(os.path.join(sourcePath, item), os.path.join(targetPath, item)))
            #shutil.copy(sourcePath, targetPath)
            #print ("\n Copying lib: %s <--> %s\n "%(sourcePath, targetPath))

        #原包有armeabi-v7a目录
        if os.path.exists(self.targetBinaryV7Path):

            #sourcePath =  os.path.join(self.sourceBinaryV7Path, globalValues.IsProtect)
            #targetPath = os.path.join(self.targetBinaryV7Path, globalValues.IsProtect)
            sourcePath =  self.sourceBinaryV7Path
            targetPath = self.targetBinaryV7Path
            for item in os.listdir(sourcePath):
                shutil.copy(os.path.join(sourcePath, item), os.path.join(targetPath, item))
                print ("\n Copying lib: %s <--> %s\n "%(os.path.join(sourcePath, item), os.path.join(targetPath, item)))
            #shutil.copy(sourcePath, targetPath)
            #print ("\n Copying lib: %s <--> %s\n " %(sourcePath, targetPath))
        print ("\n Binary file Copy Succed ... \n ")

##end

