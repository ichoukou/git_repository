# -*- encoding:utf-8 -*-

from ass_module_dynamic import AssDynamic
from ass_module_keyword import AssKeyword
from ass_module_dex_analysis import AssDexAnalysis
from ass_module_decompile import AssDecompile
from ass_module_re import AssRe
from ass_module_dtjc import AssD
from ass_module_debug import AssDebug
from ass_module_tamper import AssTamper
from ass_module_checkso import AssCheckSo
from ass_report import AssReport
from ass_adsViewAndWebViewCheck import AdsViewCheck
from ass_virusCheck import VirusCheck
import sys, traceback, os

if __name__=="__main__":                                      # 程序入口
    if(len(sys.argv) >= 2):                                    #检查参数
        try:
            report = AssReport()

            report.modules.append(AssDynamic(report))           #动态检查模块 #安装
            report.modules.append(AssD(report))
            report.modules.append(AssCheckSo(report))           #so文件检查   smali
            report.modules.append(AssDebug(report))             #反调试检查     #卸载
            
            ###report.modules.append(AssRe(report))#关键点检测  二选一 （效率高，漏报高）
            ###report.modules.append(AssKeyword(report))#关键点检测 （效率稍低，漏报低）
            
            report.modules.append(AssTamper(report))#防篡改检查
            report.modules.append(AssDecompile(report))
            report.modules.append(AssDexAnalysis(report))

            report.modules.append(AdsViewCheck(report))         #检测广告

            ###report.modules.append(VirusCheck(report))           #检测病毒

            exitCode = report.main()
            print "RESULT:" + str(exitCode)
            sys.exit(exitCode)
        except Exception as ex:
            print ex.message
            print traceback.print_exc()
            print "ERROR:EXCEPT"
            sys.exit(-1)
    else:                                                       #输入提示
        print("usage: %s [apk_file] \n")
        print("Thanks !!")
        print "ERROR:ELSE"
        sys.exit(-1)
