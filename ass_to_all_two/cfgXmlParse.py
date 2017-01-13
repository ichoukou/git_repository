#coding:utf8
import xml.dom.minidom
import os
import platform

sysstr = platform.system()
class cfgXmlParse:
    def __init__(self, manifest, config):
        self.file_path = manifest
        self.xml_result = {}
        self._pkgname = {}
        self._list_application = []
        self._xml_string = {}
        self.config = config

    def insert_Dict(self, dict, key, value):
        dict[key] = value

    #提取manifest.xml里面的元素
    def read_XML(self, file_path):
        print ("\n " + file_path + "\n ")

        dom = xml.dom.minidom.parse(file_path)
        _XmlDom = dom
        root = dom.documentElement

        #获取package name
        strPackageName = root.getAttribute('package')
        #解析package name
        if(strPackageName.find('@string/') >= 0):
            strPackageName = self._xml_string[strPackageName.split('/')[1]]
        self.insert_Dict(self.xml_result, 'package_name', strPackageName)
        _ManifestRoot = _XmlDom.firstChild

        # 获取versionName
        versionName = root.getAttribute('android:versionName')
        #解析versionName
        if(versionName.find('@string/') >= 0):
            versionName = self._xml_string[versionName.split('/')[1]]
        self.insert_Dict(self.xml_result, 'versionName', versionName)

        # 获取application name
        application_root = _ManifestRoot.getElementsByTagName('application')

        # 获取application label
        try:
            application_label = application_root[0].getAttribute('android:label')
        except:
            application_label = ""

        # 解析application_label
        if (application_label.find('@string/') >= 0):
            application_label = self._xml_string[application_label.split('/')[1]]

        self.insert_Dict(self.xml_result, 'application_label', application_label.encode('utf8'))

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
                    self._xml_string[string_index.getAttribute('name')] = string_index.childNodes[0].data
 
