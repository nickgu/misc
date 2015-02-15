#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import time
import sys
import c_kvdict
import logging

class KVDict:
    def __init__(self):
        self.__dict_handle = c_kvdict.create()
        logging.info('GET C_KVDICT : handle=%d' % self.__dict_handle)

    def load(self, flist):
        # change a filename to a list.
        if not isinstance(flist, list):
            flist = [ flist ]
        fcnt = len(flist)
        c_kvdict.load(self.__dict_handle, fcnt, flist, True )

    def find(self, key):
        return c_kvdict.find(self.__dict_handle, key)

    def has(self, key):
        return c_kvdict.has(self.__dict_handle, key)

    def write_bin(self, output_file):
        return c_kvdict.write_mem_bin(self.__dict_handle, output_file)

    def load_bin(self, input_file):
        return c_kvdict.load_mem_bin(self.__dict_handle, input_file)


class FileIndexKVDict:
    def __init__(self):
        self.__dict_handle = c_kvdict.create()
        logging.info('GET C_KVDICT : handle=%d' % self.__dict_handle)

    def load(self, flist):
        # change a filename to a list.
        if not isinstance(flist, list):
            flist = [ flist ]
        fcnt = len(flist)
        c_kvdict.load(self.__dict_handle, fcnt, flist, False )

    def load_index(self, index_file, file_list):
        # change a filename to a list.
        if not isinstance(file_list, list):
            file_list = [ file_list ]
        fcnt = len(file_list)
        return c_kvdict.load_index_and_files(
                self.__dict_handle, index_file, len(file_list), file_list)

    def write_index(self, output_file):
        return c_kvdict.write_index( self.__dict_handle, output_file )


    def find(self, key):
        return c_kvdict.find(self.__dict_handle, key)

    def has(self, key):
        return c_kvdict.has(self.__dict_handle, key)


if __name__=='__main__':
    from pygsm.arg import *
    arg = Arg()
    arg.str_opt('bin', 'i', 'load bin list')
    arg.str_opt('file_list', 'f', 'file list.')
    arg.str_opt('dump_bin', 'b', 'dump memory dict to bin')
    opt = arg.init_arg()

    d = KVDict()
    beg = time.time()
    if opt.bin:
        d.load_bin(opt.bin)
    else:
        d.load(opt.file_list)
    end = time.time()
    during_time = end - beg
    logging.info('Load over. loading time = %.4f(s)' % during_time)

    if opt.dump_bin:
        t = time.time()
        d.write_bin(opt.dump_bin)
        logging.info('dumping time : %.4f(s)' % (time.time() - t))
        sys.exit(0)

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
