# -*- coding:utf-8 -*-

import json
import codecs
import chardet
import sys
import ass_config
from reportlab.lib.units import inch
from reportlab.platypus import Spacer, Table, flowables
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Image

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import itemImpl
import itemConfigs

fontName = 'msyh'
defColors = ["yellow", "orange", "red", "green"]

#preName = '@'
pieNameTotal = 'chartTotal.png'
pieNameSource = 'chartSource.png'
pieNameData = 'chartData.png'
pieNameVul = 'chartVul.png'
pieNameEmu = 'chartEmu.png'

totalDistrib = 'total.png'
classDistrib = 'class.png'

islinux = (sys.platform != "win32")
if islinux:
    fontsPath = ass_config.pinggu_dir + '/tool_linux/STZHONGS.TTF'
else:
    fontsPath = ass_config.pinggu_dir + '/tool_win/STZHONGS.TTF'
zhfont = mpl.font_manager.FontProperties(fname=fontsPath)

#mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class RiskCount:
    def __init__(self, lowTotal, middleTotal, highTotal):
        self.low = 0
        self.middle = 0
        self.high = 0

        self.lowTotal = lowTotal
        self.middleTotal = middleTotal
        self.highTotal = highTotal

    #lvlID: 0-low 1-middle 2-high
    def setCount(self, v, lvlID):
        if lvlID == 0:
            self.low = v
        elif lvlID == 1:
            self.middle = v
        elif lvlID == 2:
            self.high = v
        else:
            raise Exception('unknown lvlID')

    def getCount(self, lvlID):
        if lvlID == 0:
            return self.low
        elif lvlID == 1:
            return self.middle
        elif lvlID == 2:
            return self.high
        else:
            raise Exception('unknown lvlID')

    def getTotalCount(self, lvlID):
        if lvlID == 0:
            return self.lowTotal
        elif lvlID == 1:
            return self.middleTotal
        elif lvlID == 2:
            return self.highTotal
        else:
            raise Exception('unknown lvlID')


class ItemManager:
    def __init__(self):
        self.isValid = True
        self.isSignOK = True
        self.showHand = True
        self.listShowHand = True

        self.appName = u'无'
        self.appVersion = u'无'
        self.appPackageName = u'无'
        self.fileSize = u'无'
        self.md5 = u'无'
        self.signInfo = u'无'
        self.appType = u'无'
        self.checkResult = u'无'
        self.resultDetail = u'无'*300

        self.checkStartTime = u'2016-12-30 21:44'
        self.checkEndTime = u'2016-12-30 22:55'

        self.checkShell = u'无'

        self.totalScore = 0

        self.dictRiskCount = {
            0 : RiskCount(9, 3, 0),              #应用安全
            1 : RiskCount(4, 7, 4),              #源码安全
            2 : RiskCount(0, 4, 1),              #数据安全
            3 : RiskCount(1, 5, 1),              #漏洞
            4 : RiskCount(0, 0, 1),              #恶意行为
            5 : RiskCount(0, 0, 0)               #服务器
        }

        self.appItems = {}
        self.sourceItems = {}
        self.dataItems = {}
        self.vulItems = {}
        self.harmItems = {}
        self.permissionItems = {}
        self.serverItems = {}

        self.normalFontSize = 14
        self.normalStyle = ParagraphStyle(name='ListTableNormalStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.blue,leading=1.2*self.normalFontSize)
        self.normalNolinkStyle = ParagraphStyle(name='ListTableNormalNolinkStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.black,leading=1.2*self.normalFontSize)
        self.infoNolinkStyle = ParagraphStyle(name='ListTableNormalNolinkStyle',fontName=fontName,fontSize=16,textColor=colors.black,leading=1.2*self.normalFontSize)
        self.centerStyle = ParagraphStyle(name='ListTableCenterStyle',fontName=fontName,fontSize=self.normalFontSize,alignment=1,leading=1.2*self.normalFontSize)
        self.normalInfoStyle = ParagraphStyle(name='InfoNormalStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.black,leading=1.2*self.normalFontSize)

    def getPackageName(self):
        return self.appPackageName

    def toDict(self):
        result = {
            'appName':self.appName,
            'appVersion':self.appVersion,
            'appPackageName':self.appPackageName,
            'fileSize':self.fileSize,
            'md5':self.md5,
            'signInfo':self.signInfo,
            'checkResult':self.checkResult,
            'resultDetail':self.resultDetail,
            'checkStartTime':self.checkStartTime,
            'checkEndTime':self.checkEndTime,
        }

        keys = self.dictRiskCount.keys()
        keys.sort()
        keyArray = ['appRiskCount', 'sourceRiskCount', 'dataRiskCount', 'vulRiskCount', 'harmRiskCount', 'serverRiskCount']
        for key in keys:
            riskCountItem = self.dictRiskCount[key]
            result[keyArray[key]] = {'low':riskCountItem.getCount(0), 'middle':riskCountItem.getCount(1), 'high':riskCountItem.getCount(2), 'lowTotal':riskCountItem.getTotalCount(0), 'middleTotal':riskCountItem.getTotalCount(1), 'highTotal':riskCountItem.getTotalCount(2)}

        objList = [self.appItems, self.sourceItems, self.dataItems, self.vulItems, self.harmItems, self.permissionItems, self.serverItems]
        objNameList = ['appItems', 'sourceItems', 'dataItems', 'vulItems', 'harmItems', 'permissionItems', 'serverItems']
        for i in xrange(len(objList)):
            obj = objList[i]
            objName = objNameList[i]
            if obj != None and len(obj) > 0:
                result[objName] = {}
                keys = obj.keys()
                keys.sort()
                for key in keys:
                    result[objName][key] = obj[key].toDict()
        return result

    def toJson(self):
        pyObj = self.toDict()
        encoder = json.JSONEncoder(ensure_ascii=False)
        jsonObj = encoder.encode(pyObj)
        return jsonObj

    def toJsonFile(self, outFilePath = 'report.json'):
        jsonStr = self.toJson()
        with codecs.open(outFilePath, 'w', 'utf-8') as ofile:
            ofile.write(jsonStr)

    def initData(self):
        isDebug = False
        for key in itemConfigs.AppItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.AppItemDict[key], self.appItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.AppItemDict[key], self.appItems)

        for key in itemConfigs.SourceItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.SourceItemDict[key], self.sourceItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.SourceItemDict[key], self.sourceItems)

        for key in itemConfigs.DataItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.DataItemDict[key], self.dataItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.DataItemDict[key], self.dataItems)

        for key in itemConfigs.VulItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.VulItemDict[key], self.vulItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.VulItemDict[key], self.vulItems)

        for key in itemConfigs.HarmItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.HarmItemDict[key], self.harmItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.HarmItemDict[key], self.harmItems)

        for key in itemConfigs.ServerItemDict.keys():
            if isDebug:
                item = itemImpl.NormalItem(key, itemConfigs.ServerItemDict[key], self.serverItems)
                item.setState(True)
            else:
                itemImpl.NormalItem(key, itemConfigs.ServerItemDict[key], self.serverItems) 

        if isDebug:
            i = 0
            for key in itemConfigs.PermissionItemDict.keys():
                if i < 34:
                    itemImpl.PermissonItem(key, itemConfigs.PermissionItemDict[key], self.permissionItems)
                i += 1

        if isDebug:
            self.dictRiskCount[0].setCount(3, 0)
            self.dictRiskCount[0].setCount(1, 1)
            self.dictRiskCount[0].setCount(0, 2)

            self.dictRiskCount[1].setCount(2, 0)
            self.dictRiskCount[1].setCount(3, 1)
            self.dictRiskCount[1].setCount(2, 2)

            self.dictRiskCount[2].setCount(0, 0)
            self.dictRiskCount[2].setCount(2, 1)
            self.dictRiskCount[2].setCount(1, 2)

            self.dictRiskCount[3].setCount(0, 0)
            self.dictRiskCount[3].setCount(1, 1)
            self.dictRiskCount[3].setCount(1, 2)

            self.dictRiskCount[4].setCount(0, 0)
            self.dictRiskCount[4].setCount(1, 1)
            self.dictRiskCount[4].setCount(1, 2)

    def updateAppItem(self, itemID, state, detail=u'无',num=0):
        if self.appItems == None or not(self.appItems.has_key(itemID)):
            return False
        self.appItems[itemID].setState(state,num)
        self.appItems[itemID].updateDetail(detail)
        lvl = self.appItems[itemID].score - 1
        v = self.dictRiskCount[0].getCount(lvl)
        self.dictRiskCount[0].setCount(v+1, lvl)
        self.totalScore += self.appItems[itemID].score

        return True

    def getRealCount(self,items):
        # realCount = 0
        # for i in xrange(5):
        #     realCount += self.dictRiskCount[i].getCount(lvlID)
        # return realCount
        lowCount, midCount, highCount = 0, 0, 0
        if items != None and len(items) > 0:
            ids = self.sortBySortId(items, 0)
            for key in ids:
                pItem = items[key]
                if pItem.type == 0 and pItem.state:
                    print pItem.name + '**********'+pItem.level + '*********'
                    if pItem.score == 1:
                        lowCount += 1
                    elif pItem.score == 2:
                        midCount += 1
                    elif pItem.score == 3:
                        highCount += 1
        return [lowCount, midCount, highCount]






    def updateSourceItem(self, itemID, state, detail=u'无',num=0):
        if self.sourceItems == None or not(self.sourceItems.has_key(itemID)):
            return False
        self.sourceItems[itemID].setState(state,num)
        self.sourceItems[itemID].updateDetail(detail)
        lvl = self.sourceItems[itemID].score - 1
        v = self.dictRiskCount[1].getCount(lvl)
        self.dictRiskCount[1].setCount(v+1, lvl)
        self.totalScore += self.sourceItems[itemID].score
        return True

    def updateDataItem(self, itemID, state, detail=u'无',num=0):
        if self.dataItems == None or not(self.dataItems.has_key(itemID)):
            return False
        self.dataItems[itemID].setState(state,num)
        self.dataItems[itemID].updateDetail(detail)
        lvl = self.dataItems[itemID].score - 1
        v = self.dictRiskCount[2].getCount(lvl)
        self.dictRiskCount[2].setCount(v+1, lvl)
        self.totalScore += self.dataItems[itemID].score
        return True

    def updateVulItem(self, itemID, state, detail=u'无',num=0):
        if self.vulItems == None or not(self.vulItems.has_key(itemID)):
            return False
        self.vulItems[itemID].setState(state,num)
        self.vulItems[itemID].updateDetail(detail)
        lvl = self.vulItems[itemID].score - 1
        v = self.dictRiskCount[3].getCount(lvl)
        self.dictRiskCount[3].setCount(v+1, lvl)
        self.totalScore += self.vulItems[itemID].score
        return True

    def updateHarmItem(self, itemID, state, detail=u'无',num=0):
        if self.harmItems == None or not(self.harmItems.has_key(itemID)):
            return False
        self.harmItems[itemID].setState(state,num)
        self.harmItems[itemID].updateDetail(detail)
        lvl = self.harmItems[itemID].score - 1
        v = self.dictRiskCount[4].getCount(lvl)
        self.dictRiskCount[4].setCount(v+1, lvl)
        self.totalScore += self.harmItems[itemID].score
        return True

    def updatePermissionItem(self, itemID, permissionName):
        if self.permissionItems == None:
            return False
        if itemConfigs.PermissionItemDict.has_key(itemID):
            self.permissionItems[itemID] = itemImpl.PermissonItem(itemID, itemConfigs.PermissionItemDict[itemID], self.permissionItems)
        else:
            self.permissionItems[itemID] = itemImpl.PermissonItem(itemID, itemConfigs.PermissionItemDict['5_NONE'], self.permissionItems)
            self.permissionItems[itemID].updadeDefData(permissionName)
        return True

    #type: 0-name 1-version 2-packageName 3-fileSize 4-md5 5-signInfo 6-appType 7-checkResult 8-resultDetail 9-checkStartTime 10-checkEndTime
    def updateBaseInfo(self, v, type):
        if isinstance(v, unicode):
            pass
        else:
            v = str(v)

        if isinstance(v, str):
            info = chardet.detect(v)
            v = v.decode(info['encoding'])

        if type == 0:
            self.appName = v
        elif type == 1:
            self.appVersion = v
        elif type == 2:
            self.appPackageName = v
        elif type == 3:
            self.fileSize = v
        elif type == 4:
            self.md5 = v
        elif type == 5:
            self.signInfo = v
        elif type == 6:
            self.appType = v
        elif type == 7:
            self.checkResult = v
        elif type == 8:
            self.resultDetail = v
        elif type == 9:
            self.checkStartTime = v
        elif type == 10:
            self.checkEndTime = v
        elif type == 11:
            self.checkShell = v

    def setSignFlag(self, v):
        self.isSignOK = v

    def getSignFlag(self):
        return self.isSignOK

    def setValidFlag(self, v):
        self.isValid = v

    def getValidFlag(self):
        return self.isValid

    def getResult(self):
        if not self.isValid:
            return -2

        if not self.isSignOK:
            return -3

        if self.totalScore < 1:     #安全
            return 0

        elif self.totalScore < 11:  #低危
            return 1

        elif self.totalScore < 21:  #中危
            return 2

        else:                       #高危
            return 3

    def getComment(self):
        if self.totalScore < 1:     #安全
            return u'安全'

        elif self.totalScore < 11:  #低危
            return u'低危'

        elif self.totalScore < 21:  #中危
            return u'中危'

        else:                       #高危
            return u'高危'

    def collectData(self):
        pass

    #type: 0-total 1-class
    def genChartParam(self, type = 0):
        if self.dictRiskCount == None:
            raise Exception('None risk data for chart')

        if type == 0:
            datas = [0, 0, 0, 0]
            #labels = [u'低危', u'中危', u'高危', u'安全']
            for i in range(3):
                for key in self.dictRiskCount:
                    riskItem = self.dictRiskCount[key]
                    datas[i] += riskItem.getCount(i)
                    datas[3] += (riskItem.getTotalCount(i) - riskItem.getCount(i))

            return datas
        elif type == 1:
            datas = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
            for i in range(4):
                riskItem = self.dictRiskCount[i]
                datas[0][i] = riskItem.getCount(0)
                datas[1][i] = riskItem.getCount(1)
                datas[2][i] = riskItem.getCount(2)
                datas[3][i] = riskItem.lowTotal + riskItem.middleTotal + riskItem.highTotal - riskItem.getCount(0) - riskItem.getCount(1) - riskItem.getCount(2)
            return datas
        else:
            raise Exception('unknown type')

    def genChartImg(self, pieName, type):
        labels = [u'低危', u'中危', u'高危', u'安全']
        datas = self.genChartParam(type)
        plt.clf()
        if type == 0:
            for i in range(len(labels)):
                labels[i] = labels[i] + '-' + str(datas[i])
            pie = plt.pie(datas, colors=defColors, labels=labels, shadow=False)
            for font in pie[1]:
                font.set_fontproperties(zhfont)
        elif type == 1:
            N = 4
            ind = np.arange(N)
            width = 1.0 / N
            fig, ax = plt.subplots()
            rects0 = ax.bar(ind + width * 0, tuple(datas[0]), width, color=defColors[0])
            rects1 = ax.bar(ind + width * 1, tuple(datas[1]), width, color=defColors[1])
            rects2 = ax.bar(ind + width * 2, tuple(datas[2]), width, color=defColors[2])
            rects3 = ax.bar(ind + width * 3, tuple(datas[3]), width, color=defColors[3])
            ax.set_ylabel(u'数量', fontproperties=zhfont)
            ax.set_xticks(ind + width * 2)
            ax.set_xticklabels((u'应用安全', u'源码安全', u'数据安全', u'漏洞'), fontproperties=zhfont)
            ax.legend((rects0[0], rects1[0], rects2[0], rects3[0]), (u'低危', u'中危', u'高危', u'安全'), prop=zhfont)
        plt.savefig(pieName)
        plt.close()
        return pieName

    def drawChart(self, xSize, ySize, pieName):
        d = Drawing(xSize, ySize)
        im = Image(0, 0, xSize, ySize, pieName)
        d.add(im)
        return d

    def genChartTable(self, container, preName='@'):
        wlist = [3.5 * inch, 3.5 * inch]
        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('ALIGN',(0,0),(-1,-1),'CENTER'))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        self.genChartImg(preName + 'total.png', 0)
        dTotal = self.drawChart(150, 150, preName + 'total.png')

        self.genChartImg(preName + 'class.png', 1)
        dClass = self.drawChart(250, 150, preName + 'class.png')
        data = [(u'风险分布情况',u'风险分布情况'),
                (u'风险总体分布图',u'类别风险分布图'),
                (dTotal, dClass)]

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

        # if os.path.isfile(preName + 'class.png'):
        #     os.remove(preName + 'class.png')
        #
        # if os.path.isfile(preName + 'total.png'):
        #     os.remove(preName + 'total.png')

    def sortBySortId(self, items, sortType=0):
        sortList = []
        ids = items.keys()
        if sortType == 0:
            for idItem in ids:
                sort_id = int(idItem[2:])
                score = items[idItem].valueDict['score']
                type = items[idItem].valueDict['type']
                sortList.append((idItem, sort_id, score, type))

            sortList = sorted(sortList, key = lambda x: (x[3], -x[2], x[1]) )

            ids = []
            for idItem in sortList:
                ids.append(idItem[0])
        else:
            ids.sort()

        return ids

    def genStandardsTable(self, container):
        wlist = [6.5 * inch, 0.5 * inch]
        data = [(u'APP安全检测依据', u' '),
                (u'《移动应用安全检测基准》', u' '),
                (u'《移动互联网应用软件安全评估大纲》', u' '),
                (u'《信息安全技术 公共及商用服务信息系统个人信息保护指南》', u' '),
                (u'《信息安全技术 移动智能终端个人信息保护技术要求》', u' '),
                (u'《YD/T 1438-2006 数字移动台应用层软件功能要求和测试方法》', u' '),
                (u'《YD/T 2307-2011 数字移动通信终端通用功能技术要求和测试方法》', u' '),
                (u'《电子银行业务管理办法》', u' '),
                (u'《电子银行安全评估指引》', u' '),
                (u'《中国金融移动支付客户端技术规范》', u' '),
                (u'《中国金融移动支付应用安全规范》', u' ')]

        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('ALIGN',(0,0),(-1,0),'CENTER'))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))
        for i in range(len(data)):
            tableStyle.append(('SPAN',(0,i),(-1,i)))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    def genAppInfoTable(self, container):
        wlist = [1.5 * inch, 5.5 * inch]
        data = [(u'APP基本信息', u' '),
                (Paragraph(u'应用名称', self.normalInfoStyle), Paragraph(self.appName, self.normalInfoStyle)),
                (Paragraph(u'程序包名', self.normalInfoStyle), Paragraph(self.appPackageName, self.normalInfoStyle)),
                (Paragraph(u'应用版本号', self.normalInfoStyle), Paragraph(self.appVersion, self.normalInfoStyle)),
                (Paragraph(u'加固信息', self.normalInfoStyle), Paragraph(self.checkShell, self.normalInfoStyle)),
                (Paragraph(u'软件大小', self.normalInfoStyle), Paragraph(self.fileSize, self.normalInfoStyle)),
                (Paragraph(u'文件MD5', self.normalInfoStyle), Paragraph(self.md5, self.normalInfoStyle)),
                (Paragraph(u'签名信息', self.normalInfoStyle), Paragraph(self.signInfo, self.normalInfoStyle))]
                #(Paragraph(u'APP应用类型', self.normalInfoStyle), Paragraph(self.appType, self.normalInfoStyle))]

        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('ALIGN',(0,0),(-1,0),'CENTER'))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    def genAbsTable(self, container):
        if self.dictRiskCount == None:
            raise Exception('dictRiskCount == None')

        lowCount = 0
        middleCount = 0
        highCount = 0
        for key in self.dictRiskCount:
            lowCount += self.dictRiskCount[key].getCount(0)
            middleCount += self.dictRiskCount[key].getCount(1)
            highCount += self.dictRiskCount[key].getCount(2)

        wlist = [1 * inch, 2.5 * inch, 1 * inch, 1.5 * inch, 1 * inch]
        data = [(u'APP安全检测报告摘要', u' ', u' ', u' ', u' '),
                (u'应用提交时间', u' ', self.checkStartTime, u' ', u' '),
                (u'检测完成时间', u' ', self.checkEndTime, u' ', u' '),
                (u'检测完成发现的风险数量', u' ', u'高 危', highCount, u' '),
                (u'检测完成发现的风险数量', u' ', u'中 危', middleCount, u' '),
                (u'检测完成发现的风险数量', u' ', u'低 危', lowCount, u' '),
                (u'检测完成发现的风险数量', u' ', u'总 合', highCount + middleCount + lowCount, u' '),
                (u'类别', u'风险评估项', u'风险评估项', u'评估结果', u'检测方式'),]
        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('ALIGN',(0,0),(-1,0),'CENTER'))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('SPAN',(0,1),(1,1)))
        tableStyle.append(('SPAN',(0,2),(1,2)))
        tableStyle.append(('SPAN',(2,1),(-1,1)))
        tableStyle.append(('SPAN',(2,2),(-1,2)))

        tableStyle.append(('SPAN',(0,3),(1,6)))
        tableStyle.append(('VALIGN',(0,3),(1,6),'MIDDLE'))
        tableStyle.append(('SPAN',(3,3),(-1,3)))
        tableStyle.append(('SPAN',(3,4),(-1,4)))
        tableStyle.append(('SPAN',(3,5),(-1,5)))
        tableStyle.append(('SPAN',(3,6),(-1,6)))
        tableStyle.append(('ALIGN',(2,3),(2,6),'CENTER'))

        tableStyle.append(('ALIGN',(0,7),(0,-1),'CENTER'))
        tableStyle.append(('BACKGROUND',(0,7),(-1,7), colors.lightyellow))
        tableStyle.append(('VALIGN',(0,7),(0,-1),'MIDDLE'))
        tableStyle.append(('ALIGN',(1,7),(1,7),'CENTER'))
        tableStyle.append(('ALIGN',(2,7),(2,-1),'CENTER'))
        tableStyle.append(('ALIGN',(3,7),(3,-1),'CENTER'))
        tableStyle.append(('ALIGN',(4,7),(4,-1),'CENTER'))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        showHand = self.listShowHand
        appEnd = self.genListTable(data, '0', self.appItems, 0, True, 0, showHand)
        sourceEnd = self.genListTable(data, '1', self.sourceItems, appEnd, True, 0, showHand)
        dataEnd = self.genListTable(data, '2', self.dataItems, sourceEnd, True, 0, showHand)
        vulEnd = self.genListTable(data, '3', self.vulItems, dataEnd, True, 0, showHand)
        harmEnd = self.genListTable(data, '4', self.harmItems, vulEnd, True, 0, showHand)
        serverEnd = self.genListTable(data, '6', self.serverItems, harmEnd, True, 0, showHand)

        startY = 8
        if showHand:
            if appEnd > 1:
                tableStyle.append(('SPAN',(0,startY),(0,appEnd-1+startY)))
            if sourceEnd > appEnd + 1 :
                tableStyle.append(('SPAN',(0,appEnd+startY + 0),(0,appEnd+startY + 8)))
                tableStyle.append(('SPAN',(0,appEnd+startY + 9),(0,sourceEnd-1+startY)))
            if dataEnd > sourceEnd + 1 :
                tableStyle.append(('SPAN',(0,sourceEnd+startY + 0),(0,sourceEnd+startY + 13)))
                tableStyle.append(('SPAN',(0,sourceEnd+startY + 14),(0,dataEnd-1+startY)))
            if vulEnd > dataEnd + 1:
                tableStyle.append(('SPAN',(0,dataEnd+startY),(0,vulEnd-1+startY)))
            if harmEnd > vulEnd + 1:
                tableStyle.append(('SPAN',(0,vulEnd+startY),(0,harmEnd-1+startY)))
            if serverEnd > harmEnd + 1:
                tableStyle.append(('SPAN',(0,harmEnd+startY),(0,serverEnd-1+startY)))
        else:
            if appEnd > 1:
                tableStyle.append(('SPAN',(0,startY),(0,appEnd-1+startY)))
            if sourceEnd > appEnd + 1 :
                tableStyle.append(('SPAN',(0,appEnd+startY + 0),(0,sourceEnd-1+startY)))
            if dataEnd > sourceEnd + 1 :
                tableStyle.append(('SPAN',(0,sourceEnd+startY + 0),(0,dataEnd-1+startY)))
            if vulEnd > dataEnd + 1:
                tableStyle.append(('SPAN',(0,dataEnd+startY),(0,vulEnd-1+startY)))
            if harmEnd > vulEnd + 1:
                tableStyle.append(('SPAN',(0,vulEnd+startY),(0,harmEnd-1+startY)))
            if serverEnd > harmEnd + 1:
                tableStyle.append(('SPAN',(0,harmEnd+startY),(0,serverEnd-1+startY)))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    #sortType : 0 数字类型比较 1 字符串比较
    def genListTable(self, data, clsID, items, iEnd, checkState=True, sortType=0, showHand=False):
        if items != None and len(items) > 0:
            ids = self.sortBySortId(items, sortType)

            # isFirst = True
            for key in ids:
                pItem = items[key]
                pHead = itemImpl.classDict[clsID]['clsName']
                pBody = None
                # if isFirst:
                #     isFirst = False
                #     pHead = itemImpl.classDict[clsID]['clsName']
                #     pHead = flowables.Preformatted(itemImpl.classDict[clsID]['clsName'],self.normalStyle,maxLineLength=5, newLineChars=' ')
                if pItem.type == 0 and pItem.state:
                    pBody = Paragraph(u'<a href=\"' + key + u'\">' + pItem.name + u'</a>',self.normalStyle)
                else:
                    pBody = Paragraph(pItem.name,self.normalNolinkStyle)

                lvlStyle = ParagraphStyle(name='lvlStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.black,alignment=1,leading=1.2*self.normalFontSize)
                pLevel = Paragraph(pItem.level,lvlStyle)

                normalStyle = ParagraphStyle(name='normalStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.black,alignment=1,leading=1.2*self.normalFontSize)
                handStyle = ParagraphStyle(name='handStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.gray,alignment=1,leading=1.2*self.normalFontSize)
                existStyle = ParagraphStyle(name='existStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.red,alignment=1,leading=1.2*self.normalFontSize)
                noexistStyle = ParagraphStyle(name='noexistStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.green,alignment=1,leading=1.2*self.normalFontSize)
                if pItem.type == 1:
                    pResult = Paragraph(pItem.result,handStyle)
                    pType = Paragraph(u'人工',normalStyle)
                else:
                    pType = Paragraph(u'自动',normalStyle)
                    if pItem.state:
                        pResult = Paragraph(pItem.result,existStyle)
                    else:
                        pResult = Paragraph(pItem.result,noexistStyle)
                if (not showHand) and pItem.type == 1:
                    return iEnd
                data.append((pHead, pBody, pLevel, pResult, pType))
                iEnd += 1
        return iEnd

    def genTables(self, items, container, sortType=0):
        if items != None and len(items) > 0:
            ids = self.sortBySortId(items, sortType)

            isFirst = True
            for key in ids:
                items[key].genTable(isFirst, container, self.showHand)
                if isFirst:
                    isFirst = False

    def genBody(self, container):
        self.genTables(self.appItems, container)
        self.genTables(self.sourceItems, container)
        self.genTables(self.dataItems, container)
        self.genTables(self.vulItems, container)
        self.genTables(self.harmItems, container)
        self.genTables(self.permissionItems, container, 1)

    def genLevelDescTable(self, container):
        wlist = [1 * inch, 1 * inch, 5 * inch]
        data = [(u'安全级别的说明', u'安全级别的说明', u'安全级别的说明'),
                (u'严重性', u'级别', u'级别描述'),
                (u'一级', u'高危', u'对应用敏感信息和核心数据的安全具有重要影响'),
                (u'二级', u'中危', u'对应用敏感信息和核心数据的安全具有一般影响'),
                (u'三级', u'低危', u'对应用敏感信息和核心数据的安全具有轻微影响'),]

        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('ALIGN',(0,0),(-1,1),'CENTER'))
        tableStyle.append(('ALIGN',(0,2),(0,-1),'CENTER'))
        tableStyle.append(('ALIGN',(1,2),(1,-1),'CENTER'))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    def genPermissionInfo(self, container):
        if self.permissionItems == None or len(self.permissionItems) == 0:
            return
        wlist = [2.3 * inch, 2.3 * inch, 2.4 * inch]
        data = [u'权限信息', u'权限信息', u'权限信息']

        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('ALIGN',(0,0),(-1,0),'CENTER'))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        normal = ParagraphStyle(name='normal',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.black,alignment=1,leading=1.2*self.normalFontSize)
        high = ParagraphStyle(name='high',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.red,alignment=1,leading=1.2*self.normalFontSize)
        middle = ParagraphStyle(name='middle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.orange,alignment=1,leading=1.2*self.normalFontSize)
        low = ParagraphStyle(name='low',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.yellow,alignment=1,leading=1.2*self.normalFontSize)

        ids = self.permissionItems.keys()
        ids.sort()
        for key in ids:
            item = self.permissionItems[key]
            if item.score == 3:
                data.append(Paragraph(u'<a href=\"' + key + u'\">' + item.name + u'</a>' + u'<br/>' + u'<a href=\"' + key + u'\">' + item.desc + u'</a>',high))
            elif item.score == 2:
                data.append(Paragraph(u'<a href=\"' + key + u'\">' + item.name + u'</a>' + u'<br/>' + u'<a href=\"' + key + u'\">' + item.desc + u'</a>',middle))
            elif item.score == 1:
                data.append(Paragraph(u'<a href=\"' + key + u'\">' + item.name + u'</a>' + u'<br/>' + u'<a href=\"' + key + u'\">' + item.desc + u'</a>',low))
            else:
                data.append(Paragraph(item.name + u'<br/>' + item.desc,normal))

        #补齐空位
        lCount = len(data) % 3
        if lCount > 0:
            for i in range(3-lCount):
                data.append(u' ')

        dataFinal = []
        for i in range(len(data)/3):
            subArray = [data[i*3], data[i*3+1], data[i*3+2]]
            dataFinal.append(tuple(subArray))

        t = Table(data=dataFinal, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    def genSummaryTable(self, container):
        wlist = [3.5 * inch, 3.5 * inch]
        data = [(u'APP安全检测报告总结', u'APP安全检测报告总结'),
                (u'应用安全综合评级', self.checkResult),
                (u'总体建议', u'总体建议'),
                (flowables.Preformatted(self.resultDetail, self.normalNolinkStyle, maxLineLength=35, newLineChars=' '), u' ')]

        tableStyle = []
        tableStyle.append(('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray))
        tableStyle.append(('BOX', (0,0), (-1,-1), 1.5, colors.black))
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,-1),self.normalFontSize))
        tableStyle.append(('BACKGROUND',(0,0),(-1,0), colors.lightblue))
        tableStyle.append(('SPAN',(0,0),(-1,0)))
        tableStyle.append(('ALIGN',(0,0),(-1,0),'CENTER'))
        tableStyle.append(('SPAN',(0,2),(-1,2)))
        tableStyle.append(('BACKGROUND',(0,2),(-1,2), colors.lightsteelblue))
        tableStyle.append(('SPAN',(0,3),(-1,3)))
        tableStyle.append(('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

    def genGroupInfo(self, container):
        wlist = [3.5 * inch, 3.5 * inch]
        info = u'北京鼎源科技有限公司（简称：鼎源科技）（www.devsource.com.cn）成立于2005年,是一家专注于移动互联网信息安全领域研究和开发的高科技企业。自2015年起，公司专注于 提供移动APP 应用安全的产品研发与服务，相继推出了鼎源APP加固盾、APP安全检测等一系列 移动安全相关的产品。'
        data = [(u'鼎源科技APP安全检测扫描平台', u' '),
                (u'（www.appbesafe.com）', u' '),
                (flowables.Preformatted(info, self.infoNolinkStyle, maxLineLength=35, newLineChars=' '), u' '),
                (u'         取得软件著作权30项，申请发明专利10多项。', u' '),
                (u'         ISO9001质量管理体系', u' '),
                (u'         中关村高新技术企业', u' '),
                (u'         北京市信技术新产品（服务）证书', u' ')]

        tableStyle = []
        tableStyle.append(('FONTNAME',(0,0),(-1,-1),fontName))
        tableStyle.append(('FONTSIZE',(0,0),(-1,0),21))
        tableStyle.append(('FONTSIZE',(0,1),(-1,-1),16))
        for i in range(len(data)):
            tableStyle.append(('SPAN',(0,i),(-1,i)))

        t = Table(data=data, colWidths=wlist, style=tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))


def genChartImg(pieName, type=0):
    labels = [u'低危', u'中危', u'高危', u'安全']
    if type == 0:
        datas = [0, 0, 0, 0]
    else:
        datas = [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]
    plt.clf()
    if type == 0:
        for i in range(len(labels)):
            labels[i] = labels[i] + '-' + str(datas[i])
        pie = plt.pie(datas, colors=defColors, labels=labels, shadow=False)
        for font in pie[1]:
            font.set_fontproperties(zhfont)
    elif type == 1:
        N = 4
        ind = np.arange(N)
        width = 1.0 / N
        fig, ax = plt.subplots()
        rects0 = ax.bar(ind + width * 0, tuple(datas[0]), width, color=defColors[0])
        rects1 = ax.bar(ind + width * 1, tuple(datas[1]), width, color=defColors[1])
        rects2 = ax.bar(ind + width * 2, tuple(datas[2]), width, color=defColors[2])
        rects3 = ax.bar(ind + width * 3, tuple(datas[3]), width, color=defColors[3])
        ax.set_ylabel(u'数量', fontproperties=zhfont)
        ax.set_xticks(ind + width * 2)
        ax.set_xticklabels((u'应用安全', u'源码安全', u'数据安全', u'漏洞'), fontproperties=zhfont)
        ax.legend((rects0[0], rects1[0], rects2[0], rects3[0]), (u'低危', u'中危', u'高危', u'安全'), prop=zhfont)
    plt.savefig(pieName)
    plt.close()

if __name__ == "__main__":
    genChartImg('total.png', 0)