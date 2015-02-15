#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import time
import sys
import kvdict
import logging

if __name__=='__main__':
    from pygsm.arg import *
    arg = Arg('Build a hash-dict for multiple_files whose first column will be key.')
    arg.var_opt('flist', 'f', 'file list.')
    arg.str_opt('index', 'i', 'index output')
    opt = arg.init_arg()

    d = kvdict.FileIndexKVDict()
    beg = time.time()
    d.load(opt.flist)
    end = time.time()
    during_time = end - beg
    logging.info('Load over. loadding time = %.4f(s)' % during_time)

    d.write_index(opt.index)

