# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

def lcs(a, b):
    ua = a.decode('gb18030')
    ub = b.decode('gb18030')
    best = 0
    for beg in range(len(ua)):
        for b in range(len(ub)):
            for l in range(len(ua)-beg-1, 0, -1):
                if l < best:
                    break
                if ua[beg:beg+l] == ub[b:b+l]:
                    best = l
    return best

import sys

if __name__ == '__main__':
    while 1:
        line = sys.stdin.readline()
        if line == '':
            break
        arr = line.strip('\n').split('\t')
        print lcs(arr[0], arr[1])
