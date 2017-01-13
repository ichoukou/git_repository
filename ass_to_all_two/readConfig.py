#coding:utf-8
import xml.dom.minidom
import os
import platform


def getCurrentScriptPath():
    currentPyFilePath = os.path.split(os.path.realpath(__file__))[0]
    return currentPyFilePath

def getConfig():
    config = {}
    sysstr = platform.system()

    if(sysstr == "Windows"):#获取windows版本配置信息
        xml_path = 'config_windows.xml'
    elif(sysstr == "Linux"):#获取linux版本配置信息
        xml_path = os.path.join(getCurrentScriptPath(), "config_linux.xml")

    root = xml.dom.minidom.parse(xml_path)#XML格式获取
    xml_root = root.documentElement
    nodes = xml_root.getElementsByTagName('data')

    for node in nodes:
        config[node.getAttribute('name')] = node.getAttribute('value')

    return config

