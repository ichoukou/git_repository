#coding: utf-8
import platform
import xml.dom.minidom
import codecs
import os
import sys
import globalValues

globalValue = globalValues.globalValues()
sysstr = platform.system()

class XMLParser:

    def __init__(self, manifest, config):
        self.file_path = manifest
        self.xml_result = {}
        self._pkgname = {}
        self._list_application = []
        self._xml_string = {}
        self.config = config

    def insert_Dict(self, dict, key, value):
        dict[key] = value

    def read_string_XML(self, tempPath):

        string_path = os.path.join(tempPath, self.config['stringPath'])
        print ("string_path: %s" %string_path)

        if not (os.path.exists(string_path)):
            print ("no string.xml \n")
            return 1

        _list_valve = []
        dom = xml.dom.minidom.parse(string_path)
        root = dom.documentElement
        string_root = root.getElementsByTagName('string')

        for string_index in string_root:
            if len(string_index.childNodes) > 0:
                # 判断文本内容没有加下划线，下划线会多一层：<u>f.10086.cn</u>
                if len(string_index.childNodes[0].childNodes) == 0:
                    # print ("\n " + string_index.getAttribute('name') + "\n ")
                    # print ("\n " + string_index.childNodes[0].data + "\n ")
                    self._xml_string[string_index.getAttribute('name')] = string_index.childNodes[0].data

    # 提取manifest.xml里面的元素
    def read_XML(self, file_path):
        print ("\n " + file_path + "\n ")

        dom = xml.dom.minidom.parse(file_path)
        _XmlDom = dom
        root = dom.documentElement

        # 获取package name
        strPackageName = root.getAttribute('package')
        self.insert_Dict(self.xml_result, 'package_name', strPackageName)
        _ManifestRoot = _XmlDom.firstChild

        # 获取versionName
        versionName = root.getAttribute('android:versionName')
        self.insert_Dict(self.xml_result, 'versionName', versionName)

        # 获取application name
        application_root = _ManifestRoot.getElementsByTagName('application')
        try:
            applicationName = application_root[0].getAttribute('android:name')
        except:
            # 如果没有application，直接返回空，所以这里好像不会被执行,只有程序运行异常的时候才会执行这里
            applicationName = ""

        # 解决相对路径
        if applicationName.strip():
            if applicationName[0] == '.':
                applicationName = strPackageName + applicationName

            # 解决相对路径，但不以‘.’开头
            if applicationName.find('.') < 0:
                applicationName = strPackageName + '.' + applicationName

        self.insert_Dict(self.xml_result, 'application', applicationName)

        # 获取application label
        try:
            application_label = application_root[0].getAttribute('android:label')
        except:
            application_label = ""

        # 解析application_label
        if (application_label.find('@string/') >= 0):
            application_label = self._xml_string[application_label.split('/')[1]]

        self.insert_Dict(self.xml_result, 'application_label', application_label.encode('utf8'))

        # 读取 mainActivity
        act_root = _ManifestRoot.getElementsByTagName('activity')
        mainActivity = ''
        mainActivityFind = False
        actionMainFind = False

        for act_idx in act_root:

            act_act = act_idx.getElementsByTagName('action')
            for act_act_index in act_act:
                if act_act_index.getAttribute('android:name') == 'android.intent.action.MAIN':
                    actionMainFind = True
                    break;
            # 没找到 ‘android.intent.action.MAIN’ 则不继续寻找 ‘android.intent.category.LAUNCHER’
            if not actionMainFind:
                continue;

            act_cat = act_idx.getElementsByTagName('category')
            for act_cat_index in act_cat:
                if act_cat_index.getAttribute('android:name') == 'android.intent.category.LAUNCHER':
                    mainActivityFind = True
                    mainActivity = act_idx.getAttribute('android:name')
                    break
            if mainActivityFind:
                break

        if mainActivity.strip():
            if mainActivity[0] == '.':  # 解决相对路径
                mainActivity = strPackageName + mainActivity
            if mainActivity.find('@string/',0) != -1: # name 用 @string/ 引用的情况
                mainActivity = self._xml_string[mainActivity.split('/')[1]]
            if mainActivity.find('.') < 0: # 解决相对路径，但不以‘.’开头
                mainActivity = strPackageName + '.' + mainActivity

        self.insert_Dict(self.xml_result, 'activityName', mainActivity)

    def writeConfig(self, outpath):
        config = []
        config.append('applicationName = %s\n' %self.xml_result['application_label'])
        config.append('packageName = %s\n' %self.xml_result['package_name'])
        config.append('versionName = %s\n' %self.xml_result['versionName'])

        if (sysstr == "Linux"):
            outfile = outpath + '/config.xml'
        else:
            outfile = outpath + '\\config.xml'
        print ('outfile: %s' %outfile)

        fp = file(outfile, 'w')
        fp.writelines(config)
        fp.close()

    def get_XML_Result(self, outpath):
        self.read_XML(self.file_path)
        self.writeConfig(outpath)
        return self.xml_result

