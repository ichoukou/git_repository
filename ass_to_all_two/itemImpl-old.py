# -*- coding:utf-8 -*-

from reportlab.lib.units import inch
from reportlab.platypus import Spacer, Table, flowables
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

classDict = {
    '0': {'clr':colors.lightcyan, 'clsName':u'应用安全'},
    '1': {'clr':colors.gold, 'clsName':u'源码安全'},
    '2': {'clr':colors.tomato, 'clsName':u'数据安全'},
    '3': {'clr':colors.cadetblue, 'clsName':u'漏洞'},
    '4': {'clr':colors.lightgreen, 'clsName':u'恶意行为'},
    '5': {'clr':colors.lightslategrey, 'clsName':u'权限信息'},
}

fontName = 'msyh'

class BaseItem:
    def __init__(self, itemID, valueDict, ownerDict):
        self.itemID = itemID
        self.type = valueDict['type']
        self.name = valueDict['name']
        self.desc = valueDict['desc']
        self.level = valueDict['level']
        self.harm = valueDict['harm']
        self.score = valueDict['score']

        self.result = valueDict['result']
        self.analysis = valueDict['analysis']
        self.detail = valueDict['detail']
        self.advise = valueDict['advise']
        if ownerDict != None:
            ownerDict[itemID] = self

        self.normalFontSize = 14
        clr = classDict[itemID[0]]['clr']
        self.tableStyle = [('BACKGROUND',(0,0),(-1,0), clr),
                           ('SPAN',(0,0),(-1,0)),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
                           ('FONTNAME',(0,0),(-1,-1),fontName),
                            ('FONTSIZE',(0,0),(-1,-1),self.normalFontSize),
                           ('LEADING',(0,0),(-1,-1),self.normalFontSize*1.2),
                           ('BOX', (0,0), (-1,-1), 1.5, colors.black)]

        self.normalStyle = ParagraphStyle(name='TableNormalStyle',fontName=fontName,fontSize=self.normalFontSize,leading=1.2*self.normalFontSize)
        self.centerStyle = ParagraphStyle(name='TableCenterStyle',fontName=fontName,fontSize=self.normalFontSize,alignment=1,leading=1.2*self.normalFontSize)
        self.specStyle = ParagraphStyle(name='TableSpecStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.green,leading=1.2*self.normalFontSize)

    def toDict(self):
        result = {
            'itemID':self.itemID,
            'type':self.type,
            'name':self.name,
            'desc':self.desc,
            'level':self.level,
            'harm':self.score,
            'result':self.result,
            'analysis':self.analysis,
            'detail':self.detail,
            'advise':self.advise
        }
        return result

    def genTable(self, isFirst, container, showHand=False):
        if self.type == 1 and (not showHand):
            return

        f = inch
        b = 6 * inch
        wlist = [f, b]

        data = []
        #台头
        pHead = None
        if isFirst:
            clsName = classDict[self.itemID[0]]['clsName']
            pHead = Paragraph(clsName,self.centerStyle)
        else:
            pHead = Paragraph(u'    ',self.centerStyle)
        data.append((pHead, u' '))
        maxWidth = 30
        #检测项
        pTitle = Paragraph(u'<a name=\"' + self.itemID + u'\"/>检测项',self.centerStyle)
        pTitleValue = flowables.Preformatted(self.name,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pTitle, pTitleValue))
        #风险描述
        pDesc = Paragraph(u'风险描述',self.centerStyle)
        pDescValue = flowables.Preformatted(self.desc,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pDesc, pDescValue))
        #风险级别
        pLvl = Paragraph(u'风险级别',self.centerStyle)
        pLvlValue = flowables.Preformatted(self.level,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pLvl, pLvlValue))
        #风险危害
        pHarm = Paragraph(u'风险危害',self.centerStyle)
        pHarmValue = flowables.Preformatted(self.harm,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pHarm, pHarmValue))
        #评估结论
        pRes = Paragraph(u'评估结论',self.centerStyle)
        pResValue = flowables.Preformatted(self.result,self.specStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pRes, pResValue))
        #风险分析
        pAnaly = Paragraph(u'风险分析',self.centerStyle)
        pAnalyValue = flowables.Preformatted(self.analysis,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pAnaly, pAnalyValue))
        #风险详情
        pSpec = Paragraph(u'风险详情',self.centerStyle)
        pSpecValue = flowables.Preformatted(self.detail,self.normalStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pSpec, pSpecValue))
        #处理建议
        pAndvice = Paragraph(u'处理建议',self.centerStyle)
        pAndviceValue = flowables.Preformatted(self.advise,self.specStyle,maxLineLength=maxWidth, newLineChars=' ')
        data.append((pAndvice, pAndviceValue))

        t = Table(data=data, colWidths=wlist, style=self.tableStyle)
        container.append(t)
        container.append(Spacer(50, 5))

class PermissonItem(BaseItem):
    def __init__(self, itemID, valueDict, ownerDict):
        BaseItem.__init__(self, itemID, valueDict, ownerDict)

        self.specStyle = ParagraphStyle(name='TableSpecStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.red,leading=1.2*self.normalFontSize)

    def updadeDefData(self, name):
        self.name = name
        self.desc = u'APP将具备使用该自定义权限' + name + u'的能力'
        self.analysis = u'APP开发中开启了该自定义权限' + name
        self.detail = name


class NormalItem(BaseItem):
    def __init__(self, itemID, valueDict, ownerDict):
        BaseItem.__init__(self, itemID, valueDict, ownerDict)
        self.state = False
        self.valueDict = valueDict
        if self.type == 1:
            self.result = u'待定'
            self.analysis = u'需要进过人工审核确定该项的安全性'
            self.detail = u'无'
            self.advise = u'建议对该APP应用实施人工审核以确定该项的安全性'

    def setState(self, s):
        if self.type == 1:
            return
        self.state = s
        if self.state:
            self.result = self.valueDict['resultT']
            self.analysis = self.valueDict['analysisT']
            self.advise = self.valueDict['adviseT']
            self.specStyle = ParagraphStyle(name='TableSpecStyle',fontName=fontName,fontSize=self.normalFontSize,textColor=colors.red,leading=1.2*self.normalFontSize)

    def updateDetail(self, v):
        self.detail = v
