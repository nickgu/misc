# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import sys
import c_prod
import time

def process(last_query, vinfo):
    ttime = 0
    tcount = 0

    if last_query is None:
        return 0, 0
    vlist = vinfo.values()
    t = time.time()
    ret = c_prod.self_dot(tuple(vlist))
    dt = time.time() - t
    ttime += dt
    tcount += 1

    return tcount, ttime

if __name__ == '__main__':
    total_time = 0
    total_count = 0

    last_query = None
    vinfo = {}
    for line in sys.stdin.readlines():
        arr = line.strip('\n').split('\t')
        if len(arr)!=3:
            continue
        query, uri, v = arr
        if query != last_query:
            t1, t2 = process(last_query, vinfo)
            total_count += t1
            total_time += t2

            last_query = query
            vinfo = {}
        if uri in vinfo:
            continue
        f = []
        for tu in v.split(','):
            idx, val = tu.split(':')
            idx = int(idx)
            val = float(val)
            f.append( (idx, val) ) 
        vinfo[uri] = f

    t1, t2 = process(last_query, vinfo)
    total_count += t1
    total_time += t2

    print >> sys.stderr, 'each_process:%.4f total_time:%.4f total_count=%d' % (total_time/total_count, total_time, total_count)
