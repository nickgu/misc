#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import math

def KLDivergence(dis_A, dis_B):
    '''
        get KLDivergence on distribution A.
    '''
    da = {}
    db = {}
    sa = sum(map(lambda x:x[1], dis_A))
    sb = sum(map(lambda x:x[1], dis_B))
    for key, cnt in dis_A:
        da[key] = cnt
    for key, cnt in dis_B:
        db[key] = cnt
    ret = 0.0
    for key, cnt_a in da.iteritems():
        cnt_b = db.get(key, 1)
        prob = cnt_a * 1.0 / sa
        prob_B = cnt_b * 1.0 / sb
        #print '%s : %.3f %.3f' % (key, prob, prob_B)
        ret += prob * math.log(prob / prob_B)
    return ret

if __name__=='__main__':
    import sys 
    dis_a = []
    dis_b = []
    for line in file(sys.argv[1]).readlines():
        arr = line.strip('\n').split('\t')
        if len(arr)<2:
            continue
        dis_a.append( (arr[0], float(arr[1])) )
    for line in file(sys.argv[2]).readlines():
        arr = line.strip('\n').split('\t')
        if len(arr)<2:
            continue
        dis_b.append( (arr[0], float(arr[1])) )
    kl = KLDivergence(dis_a, dis_b)
    print 'KL=%.4f' % kl


    '''
    last_key = None
    store_lines = []
    while 1:
        line = sys.stdin.readline()
        if line == '':break
        arr = line.strip('\n').split('\t')
        if len(arr)!=4:
            continue
        key = arr[0]
        if key!=last_key:
            if last_key:
                process(last_key, store_lines)
            store_lines = []
            last_key = key
        store_lines.append(arr[1:4])

    if last_key:
        process(last_key, store_lines)
    '''


'''
def process(last_key, store_lines):
    dis_a = []
    dis_b = []
    for label, var, cnt in store_lines:
        if label == 'A':
            dis_a.append( (var, float(cnt)) )
        if label == 'B':
            dis_b.append( (var, float(cnt)) )
    kl = KLDivergence(dis_a, dis_b)
    print '%s\tKL=%.4f' % (last_key, kl)
'''
