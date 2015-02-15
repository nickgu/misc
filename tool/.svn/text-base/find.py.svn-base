#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys

if __name__=='__main__':
    query_set = set(map(lambda x:x.strip('\n'), file('query.txt').readlines()))
    sys.stderr.write('Load query set over [%d]\n' % len(query_set))
    while 1:
        line = sys.stdin.readline()
        if line == '' : break
        arr = line.strip('\n').split('\t')
        if arr[0] in query_set:
            print line.strip('\n')
