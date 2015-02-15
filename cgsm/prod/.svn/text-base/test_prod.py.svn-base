# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import sys
import c_prod
import time

total_time = 0
total_count = 0

def process(last_query, vinfo):
    global total_time
    global total_count

    if last_query is None:
        return 
    vlist = vinfo.values()
    t = time.time()
    ret = c_prod.self_dot(tuple(vlist))
    dt = time.time() - t
    total_time += dt
    total_count += 1

if __name__ == '__main__':
    global total_time
    global total_count

    last_query = None
    vinfo = {}
    for line in sys.stdin.readlines():
        arr = line.strip('\n').split('\t')
        if len(arr)!=3:
            continue
        query, uri, v = arr
        if query != last_query:
            process(last_query, vinfo)
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

    process(last_query, vinfo)


    print >> sys.stderr, 'each_process:%.4f total_time:%.4f total_count=%d' % (total_time/total_count, total_time, total_count)
