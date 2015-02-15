#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#
#   V2.0:
#       support multi-fields.
#       support 'fid:value' format.
#       support seperator.
#
#   V1.0:
#       input two columns:
#           X[tab]Y
#       calc: 
#           corel = sum( (x-xavg)*(y-yavg) ) / [sqrt(sum((x-xavg)^2)) * sqrt(sum(y-yavg)^2)]
#

import sys
import math

def calc_corel(X, Y):
    avg_X = sum(X) / len(X)
    avg_Y = sum(Y) / len(Y)
    tX = map(lambda x:x-avg_X, X)
    tY = map(lambda y:y-avg_Y, Y)
    up = sum( map(lambda x:x[0]*x[1], zip(tX, tY)) )
    if up == 0.0:
        return up
    corel = up / (math.sqrt(sum(map(lambda x:x*x, tX))) * math.sqrt(sum(map(lambda y:y*y, tY))))
    return corel

if __name__=='__main__':
    sep='\t'
    if len(sys.argv)>1:
        sep = sys.argv[1]
    X = []
    Ys = []
    first_line = True
    field_name = None
    while 1:
        line = sys.stdin.readline()
        if line == '':
            break
        arr = line.strip('\n').split(sep)
        if first_line:
            first_line = False
            for i in range(len(arr)-1):
                Ys.append( [] )
            if not arr[0][0].isdigit():
                field_name = arr
                continue

        if len(arr)!=len(Ys) + 1:
            continue
        x = arr[0]
        if ':' in x: x = x.split(':')[1]
        X.append( float(x) )

        fid = 0
        for y in arr[1:]:
            if ':' in y: y = y.split(':')[1]
            Ys[fid].append( float(y) )
            fid += 1

    fid = 0
    corel_list = []
    for Y in Ys:
        corel = calc_corel(X, Y)
        #print corel
        if field_name:
            print >> sys.stderr, 'COREL_%s : %.4f' % (field_name[fid+1], corel)
        else:
            print >> sys.stderr, 'COREL_%d : %.4f' % (fid, corel)
        corel_list.append( [fid, corel] )
        fid += 1
    corel_list = sorted(corel_list, key=lambda x:-abs(x[1]))
    print >> sys.stderr, 'TOP 5 COREL:'
    for fid, value in corel_list[:5]:
        if field_name:
            print >> sys.stderr, 'ORIGINAL_FIELD_%s : %.3f' % (field_name[fid+1], value)
        else:
            print >> sys.stderr, 'ORIGINAL_FIELD_%d : %.3f' % (fid+1, value)




