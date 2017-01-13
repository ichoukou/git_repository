#coding: utf-8
'''
'''
import json


class JSONParser:
    def jx_json(self,apk_file):
        print('你好！')
        jsf=open(apk_file + ".json", 'r')
        res=json.load(apk_file + ".json")
        print(res['result']['lastValue'])
        jsf.close()
 

#----------------------------
