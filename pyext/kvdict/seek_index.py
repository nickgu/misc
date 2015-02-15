#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import time
import sys
import kvdict
import logging

if __name__=='__main__':
    from zxdb.arg import *
    arg = Arg()
    arg.var_opt('flist', 'f', 'file list.', nargs='*')
    arg.str_opt('index', 'i', 'index output')
    opt = arg.init_arg()

    d = kvdict.KVDict()
    beg = time.time()
    d.load_index(opt.index, opt.flist)
    end = time.time()
    during_time = end - beg
    logging.info('Load over. loadding time = %.4f(s)' % during_time)

    counter = 0
    beg = time.time()
    not_found = 0
    while 1:
        key = sys.stdin.readline();
        if key == '': break
        key = key.strip('\n');
        out = d.seek(key);
        if out is None:
            not_found += 1
        else:
            print '%s: %s' % (key, out)
        counter += 1
    end = time.time()

    during_time = end - beg
    if counter>0:
        avg_time = during_time / counter
        logging.info('TIME      = %.4f(s)' % during_time)
        logging.info('COUNTER   = %4d' % counter)
        logging.info('AVERAGE   = %.4f(s)' % avg_time)
        logging.info('NOTFOUND  = %4d(s)' % not_found)
