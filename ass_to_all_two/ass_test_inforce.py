# -*- coding:utf-8 -*-
'''
'''

import os
import sys
from ass_base import q

if __name__=="__main__":
    if len(sys.argv)<3:
        print("usage: ass_test_inforce.py apk_dir csv")
        exit()
    else:
        topdir = sys.argv[1]
        if os.path.isdir(topdir):
            ext_name = ".apk"
            ext_len = len(ext_name)
            for root, dirs, files in os.walk(topdir, topdown=False):
                #hanlde file
                for name in files:
                    if name[-ext_len:] == ext_name:
                        path = os.path.join(root,name)
                        os.system("python ass_module_test_inforce.py "+q(path)+" - "+q(sys.argv[2]))
        else:
            path = topdir
            os.system("python ass_module_test_inforce.py "+q(path)+" - "+q(sys.argv[2]))
            
        
                    
                    

    
    
