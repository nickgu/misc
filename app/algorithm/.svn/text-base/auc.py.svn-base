# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import sys

def AUC(predict_Y, Y, output_detail=False):
    zip_arr = sorted(zip(predict_Y, Y), key=lambda x:(-x[0], -x[1]))
    positive_count = 0
    negative_count = 0
    cur_pos_count = 0
    area = 0.0
    stat_count = 0

    all_count = len(Y)
    all_positive_count = len(filter(lambda x:x>=1.0, Y))
    
    out_cur = 0
    if output_detail:
        print >> sys.stderr, 'VALUE\tFPR\tTPR'
        print >> sys.stderr, '-\t0.00\t0.000'
    for idx, (py, y) in enumerate(zip_arr):
        if y == 1: # positive.
            cur_pos_count += 1
        else:
            stat_count += 1
            negative_count += 1

        if idx == len(zip_arr)-1 or zip_arr[idx+1][0] != py:
            if output_detail:
                FPR = negative_count * 1.0 / (all_count - all_positive_count)
                TPR = (positive_count + cur_pos_count) * 1.0 / all_positive_count
                if int(FPR * 20) > out_cur:
                    for i in range(out_cur, int(FPR*20)):
                        ratio = (i - out_cur + 1.0) / (int(FPR*20) - out_cur)
                        print >> sys.stderr, '%.4f\t%.2f\t%.3f' % (py, (i + 1.0)/20.0, (positive_count + cur_pos_count * ratio) * 1.0 / all_positive_count)
                    out_cur = int(FPR*20)
                inc = ((positive_count + 0.5 * cur_pos_count) / all_positive_count) * stat_count
                area += inc
                stat_count = 0
                positive_count += cur_pos_count
                cur_pos_count = 0

    return area / negative_count

if __name__ == '__main__':
    X = []
    Y = []
    for line in sys.stdin.readlines():
        arr = line.strip('\n').split('\t')
        if len(arr)<2:
            continue
        X.append( float(arr[1]) )
        Y.append( float(arr[0]) )

    print >> sys.stderr, 'Load records over. %d records loaded' % len(X)
    auc = AUC(X, Y, output_detail=True)
    print '%.5f' % auc

