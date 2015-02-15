#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 
#   Extract random data from file list.
#   usage:
#       random_querylog.py <num> [<file>]

import sys
import random

if __name__=='__main__':
    random_num = int(sys.argv[1])
    fd = sys.stdin
    fn = 'sys.stdin'
    if len(sys.argv)>=3:
        fn = sys.argv[2]
        fd = file(fn)
    print >> sys.stderr, 'random_num:%d' % random_num
    print >> sys.stderr, 'input_file:%s' % fn

    random_list = []
    while 1:
        line = fd.readline()
        if line == '': 
            break
        if len(random_list) < random_num:
            random_list.append(line.strip('\n'))
        else:
            random_list[ random.randint(0, random_num-1) ] = line.strip('\n')

    for line in random_list:
        print line

