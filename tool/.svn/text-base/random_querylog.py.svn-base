#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 
#   Extract random query from querylog
#   querylog format:
#       query, freq, other info.
#
#   usage:
#       random_querylog.py <file> <num>

import sys
import random
if __name__=='__main__':
    if len(sys.argv)!=3:
        print >> sys.stderr, 'Usage: %s <file> <num>' % sys.argv[0]
        os.exit(-1)

    querylog_filename = sys.argv[1]
    random_num = int(sys.argv[2])
    random_list = []
    total_freq = 0
    # first scan.
    fd = file(querylog_filename)
    while 1:
        line = fd.readline()
        if line == '': break
        arr = line.strip('\n').split('\t')
        query, freq = arr[:2]
        total_freq += int(freq)
    fd.close()
    print >> sys.stderr, 'First scan over : %d' % total_freq

    # make output id.
    for i in range(random_num):
        r = random.randint(0, total_freq-1)
        random_list.append( [i, r, None] )
    random_list = sorted(random_list, key=lambda x:x[1])
    print >> sys.stderr, 'Generate seed over.'
    
    # second scan.
    fd = file(querylog_filename)
    cur_pos = 0
    accumulated = 0
    while 1:
        line = fd.readline()
        if line == '': break
        arr = line.strip('\n').split('\t')
        query, freq = arr[:2]
        accumulated += int(freq)
        while cur_pos<len(random_list) and random_list[cur_pos][1]<accumulated:
            random_list[cur_pos][2] = query
            cur_pos += 1
    fd.close()
    print >> sys.stderr, 'Second scan over.'
        
    random_list = sorted(random_list, key=lambda x:-x[0])
    for i, seed, query in random_list:
        print query




