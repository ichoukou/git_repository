# -*- coding:utf-8 -*-
'''
'''

from ass_module import AssModule
import ass_base

class AssBase(AssModule):
    def __init__(self):
        super(AssBase, self).__init__()
        self.print_report = False
        
    def run(self):
        super(AssBase, self).run()
        ass_base.write_file(self.apk_file+".xml", "applicationName = "+self.report.report.basic.appName+"\npackageName = "+self.report.report.basic.packageName+"\nversionName = "+self.report.report.basic.appVersion)

if __name__=="__main__":
    AssBase().main()
