#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

from ulpackreader import *

if __name__=='__main__':
    reader=ULPackReader(sys.stdin)
    for item in reader.read():
        url = item.kv.Url
        cont = pack.body
        cont.replace('\t', '')
        cont.replace('\n', '')


