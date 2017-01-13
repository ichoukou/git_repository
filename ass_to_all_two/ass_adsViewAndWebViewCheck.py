#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
from ass_module import AssModule
reload(sys)


class AdsViewCheck(AssModule):

    adsList = [
         'com.suizong.mobplate',
         'com.wooboo',
         'com.qq.e.ads',
         'com.baidu.mobads',
         'com.google.android.gms.ads',
         'com.google.ads.AdActivity',
         'com.inmobi.ads',
         'cn.domob.android.ads',
         'com.mobisage',
         'cn.smartmad.ads',
         'com.sixth.adwoad',
         'com.fractalist.sdk',
         'cn.aduu',
         'com.smaato.SOMA',
         'com.izp.theia',
         'com.renren.rmob',
         'com.mobfox',
         'com.otomod',
         'com.adshow',
         'net.youmi',
         'com.zestadz',
         'com.mdotm',
         'com.millennialmedia',
         'com.greystripe',
         'com.eadver',
         'net.miidi.ad',
         'com.taobao.munion',
         'com.wqmobile',
         'com.chance.ads',
         'cn.guomob',
         'com.adarrive',
         'cn.com.pingcoo',
         'cn.lomark',
         'com.guohead.mix',
         'com.vungle',
         'com.adwalker.wall',
         'com.iisensemob',
         'com.adsame',
         'com.chartboost',
         'com.adchina',
         'com.energysource.szj',
         'cn.appmedia.ad',
         'com.android.mis',
         'MobWin',
         'com.wiyun',
         'com.vpon.adon',
         'com.mt.airad',
         'com.ignitevision.android',
         'com.l.adlib_android',
         'com.winad.android',
         'com.izp',
         'com.umengAd',
         'com.lmmob',
         'cn.waps',
         'com.ad.android.sdk.api.AdWallActivity',
         'com.jmp.sfc.ui.DSWV',
         'com.j.p.ui.MA',
         'com.newqm.sdkoffer',
         'com.xyz',
         'com.bb.dd.Browser',
         'com.imopan',
         'com.wandoujia.ads.sdk',
         'com.mediav.ads',
         'com.jp.wall.AppSDKWallActivity',
         'com.epkg',
         'com.pkfg.k',
         'com.pfkg.b',
         'com.bpkg.m',
         'com.kd.a',
         'com.bodong.dianjinweb',
         'com.baidu.ops.appunion.sdk',
         'com.momead.sdk.MomeadActivity',
         'com.iadmob.sdk.view.IadmobActivity',
         'com.madhouse.android.ads',
         'com.casee.adsdk',
         'com.iflytek.voiceads',
         'net.doujin.android.DJActivity',
         'pop.doujin.android.pop.PopReceiver',
         'com.datouniao.AdPublisher.AdsService',
         'com.mj.MjService',
         'com.huayu.analytics',
         'net.adways.appdriver2',
         'cc.admore.mobile.ads.AdBrowser',
         'com.zy.phone.sdk.SDKActivity',
         'com.juzi.main.TheAdVirtualGoods',
         'com.jirbo.adcolony',
         'com.dlnetwork.DianleGoogleActivity',
         'cn.vm.ad.OffersWebView',
         'com.ZMAD',
         'com.dianru.sdk.AdActivity',
         'com.dianru.push.NotifyActivity',
         'com.appflood.mraid.MraidBrowserActivity',
         'com.duoguo.logic',
         'com.huawei.hiad.core.BrowserActivity',
         'com.sevensdk.ge.service.DownService',
         'com.afcgxiix.wall',
         'com.bwovfvmg.b',
         'com.dnphodtz.p',
         'com.lerdian',
         'com.longmob.pet.LongActivity',
         'com.wbno.minter.vfrist',
         'com.markcai.ket',
         'com.tapjoy',
         'com.baixing.ui.activity',
         'com.upush.sdk.PushActivity',
         'com.ads8.AdActivity',
         'com.myapp.jfq.JFQActivity',
         'com.zhuamob.recommendsdk',
         'com.adwo.adsdk',
         'com.rrgame',
         'com.example.loadermanage.LMA',
         'com.kuaiyou.adbid',
         'jp.adlantis.android',
         'com.adzhidian',
         'com.punchbox.ads',
         'com.suizong.mobile.ads',
         'com.donson.momark',
         'com.jy.func',
         'com.yl.dianqu',
         'com.xiaomi.mipush.sdk',
         'com.prop.move.extension',
         'com.igexin.sdk',
         'com.getui.pmpsdk'
        ]                                      #添加广告特征

    adsName = [
        u'随踪',
        u'哇棒',
        u'广点通',
        u'百度',
        u'Admob',
        u'Admob',
        u'InMobi',
        u'多盟',
        u'艾德思奇',
        u'亿动智道',
        u'AdWo安沃',
        u'飞云',
        u'优友',
        u'Smaato',
        u'北京移动',
        u'人人移动广告联盟',
        u'MobFox',
        u'百灵欧拓',
        u'ADSHOW',
        u'有米',
        u'ZestADZ',
        u'MdotM',
        u'Millennial Media',
        u'Greystripe',
        u'易积分(亿玛)',
        u'米迪',
        u'TanX移动',
        u'帷千',
        u'畅思广告',
        u'果盟',
        u'智迅',
        u'宾谷',
        u'点媒',
        u'MIX智游汇(果合)',
        u'Vungle',
        u'行云',
        u'众感传媒',
        u'传漾',
        u'Chartboost',
        u'易传媒',
        u'AdTouch',
        u'AppMedia',
        u'道有道',
        u'腾讯聚赢',
        u'微云',
        u'Vpon(威朋)',
        u'airAD',
        u'天幕',
        u'LSense百分通联',
        u'赢告',
        u'亿赞普',
        u'友盟',
        u'力美',
        u'万普',
        u'鹰眼移动广告',
        u'聚米广告',
        u'聚米广告',
        u'趣米广告',
        u'畅想广告',
        u'贝多广告',
        u'磨盘时代移动广告',
        u'豌豆荚移动广告',
        u'聚效广告',
        u'巨朋广告',
        u'酷果',
        u'酷果酷仔',
        u'酷果',
        u'酷果媒体',
        u'酷果自定义',
        u'点金广告',
        u'百度百通',
        u'多米广告',
        u'爱告广告',
        u'易动智道',
        u'架势无线',
        u'讯飞移动广告',
        u'91斗金广告',
        u'91斗金广告',
        u'大头鸟广告',
        u'抓猫广告平台',
        u'优效',
        u'爱普动力',
        u'安盟移动广告',
        u'中亿传媒',
        u'桔子广告',
        u'AdColony',
        u'Dianjoy点乐',
        u'微盟',
        u'指盟',
        u'点入',
        u'点入',
        u'appflood',
        u'D.push',
        u'华为聚点广告',
        u'第七传媒',
        u'豆盟积分墙',
        u'豆盟广告条',
        u'豆盟推送',
        u'乐点',
        u'掌龙互动',
        u'手心联盟积分墙',
        u'手心联盟推送',
        u'tapjoy',
        u'百姓网',
        u'优推',
        u'有盟',
        u'小麦网积分墙',
        u'小麦网推荐广告横幅',
        u'AdWo安沃',
        u'Ader艾德尔广告',
        u'千速广告',
        u'AdView',
        u'Adlantis',
        u'指点',
        u'触控',
        u'云云',
        u'Momark',
        u'炅友传媒',
        u'炅友传媒',
        u'小米推送',
        u'panda',
        u'个灯(aBeacon)',
        u'个灯(aBeacon)'
        ]                          #添加广告名称
    SmaliList = []
    SmaliList2 = []
    AdsList = []
    # Webviewlist = []

    def run(self):
        super(AdsViewCheck, self).run()
        if not self.report.getValidFlag():
            return False

        try:
            self.smali(True)  #获取文件源码
            for root, dirs, files in os.walk(self.smali_dir):
                for fileName in files:
                    if fileName.endswith('.smali'):
                        tmp = os.path.join(root, fileName)
                        self.SmaliList2.append(tmp)
                        self.SmaliList.append(tmp.replace('\\', '.'))


            #检测广告
            self.report.progress("广告检测")
            for i in range(len(self.adsList)):
                for j in range(len(self.SmaliList)):
                    if self.SmaliList[j].find(self.adsList[i]) > -1:
                        self.AdsList.append(self.adsName[i])
                        break

            #检测webview
            # self.report.progress("WebView检测")
            # for i in xrange(len(self.SmaliList2)):
            #     with open(self.SmaliList2[i], 'rb+') as fp:
            #         strbuf = fp.read()
            #     if strbuf.find('addJavascriptInterface') > -1:
            #         self.Webviewlist.append(re.sub(r'\\', r'.', self.SmaliList2[i][len(self.smali_dir):]))


        except:
            self.report.LOG_OUT("can not reback apk")

        self.clean()
        if len(self.AdsList) != 0:
            res = (','.join(self.AdsList)).encode('utf-8')
            print res
            self.report.setItem('4_0', "存在以下厂商的广告:" + res + "广告")     #广告
            # f = open("ads.txt", 'a')
            # f.write(self.apk_file + "----------" + res.decode('utf-8'))
            # f.write('\n')
            # f.close()
            return res

        # if len(self.Webviewlist) != 0:
        #     print "WebView存在安全问题"
        #     self.report.setItem('0_20', "WebView存在安全问题")     #WebView存在安全问题


if __name__ == '__main__':
    AdsViewCheck().main()














