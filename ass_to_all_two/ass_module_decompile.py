# -*- coding:utf-8 -*-

import os
import ass_base
import ass_report

from ass_module import AssModule

class AssDecompile(AssModule):
    def init(self, argv):
        super(AssDecompile, self).init(argv)
        self.abc = []
        self.decompilep = []

    def decompile(self, force=False):
        print "apk decompile begin"
        self.dex2jar(force)
        print "decompile end"

    def walk(self, ext):
        topdir = os.path.join(self.apk_file + "." + ext, ext)
        ext_name = "." + ext
        ext_len = len(ext_name)
        for root, dirs, files in os.walk(topdir, topdown=False):
            if root.find(os.path.join(topdir, "android")) == 0:
                continue
            for name in files:
                if name[-ext_len:] == ext_name:
                    if len(name[:-ext_len]) == 1 and name[:-ext_len] != 'R':
                        self.abc.append(name)
                    path = os.path.join(root, name)
                    disp_path = path.replace(topdir, '')
                    self.decompilep.append(disp_path)

    def run(self):
        super(AssDecompile, self).run()
        self.decompile(True)
        self.walk("java")
        if len(self.decompilep) > 0:
            self.report.setItem('1_3', ', '.join(self.decompilep) + ',...')

        if len(self.abc) > 3:
            self.report.setItem('1_2', ', '.join(self.decompilep) + ',...')
