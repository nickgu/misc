#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import math
from sklearn import linear_model

class LRDataReader:
    def __init__(self):
        self.__FIELD_SEPERATOR = '\t'
        self.__X = []
        self.__Y = []
        self.__key_idx_table = {}
        self.__idx_key_table = []
        self.__not_finalized = True

    def __get_key_idx(self, key):
        if key not in self.__key_idx_table:
            self.__key_idx_table[key] = len(self.__key_idx_table)
        return self.__key_idx_table[key]

    def read(self, line):
        arr = line.strip('\n').split(self.__FIELD_SEPERATOR)
        label = int(arr[0])
        self.__Y.append(label)
        # process feature field.
        # data[0] : original column data.
        # data[1] : key data.
        data = []
        for col_idx, info in enumerate(arr[1:]):
            key = None
            try:
                if ':' in info:
                    key, value = info.split(':')
                    value = float(value)
                else:
                    key = '#col:%d' % (col_idx)
                    value = float(info)
            except ValueError:
                continue
            key_idx = self.__get_key_idx(key)
            data.append( (key_idx, value) )
        self.__X.append(data)

    def X(self): 
        if self.__not_finalized:
            self.finalize()
        return self.__X
    def Y(self):
        return self.__Y

    def finalize(self):
        X = []
        dim = max(self.__key_idx_table.values()) + 1
        for x in self.__X:
            d = [0.0] * dim 
            for idx, val in x:
                d[idx] = val
            X.append(d)
        self.__X = X

        self.__idx_key_table = [''] * dim
        for key, value in self.__key_idx_table.iteritems():
            self.__idx_key_table[value] = key

        for i in range(dim):
            dim_X = map(lambda x:x[i], X)
            corel = self.calc_corel(dim_X, self.__Y)
            print '%d\t%s\t%.3f' % (i, self.__idx_key_table[i], corel)
        self.__not_finalized = False

    def calc_corel(self, X, Y):
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
    file_name = '/dev/stdin'
    if len(sys.argv)>1:
        file_name = sys.argv[1]
    print >> sys.stderr, 'FILE_NAME: %s' % file_name

    clf = linear_model.LinearRegression()
    fd = file(file_name)
    reader = LRDataReader()
    line_count = 0
    while 1:
        line = fd.readline()
        if line == '':
            break
        reader.read(line)

        line_count += 1
        if line_count % 100000 == 0:
            print >> sys.stderr, 'Load %d line(s)' % line_count

    X = reader.X()
    Y = reader.Y()
    print >> sys.stderr, 'Read over. len=[%d]' % len(X)

    clf.fit(X, Y)
    print >> sys.stderr, 'Trainning over.'
    print >> sys.stderr, 'COEF: %s' % ', '.join(map(lambda x:'%.5f' % x, clf.coef_))

    predict_Y = map(lambda f:sum(map(lambda x:x[0]*x[1], zip(clf.coef_, f))), X)
    predict_corel = reader.calc_corel(Y, predict_Y)
    print >> sys.stderr, 'Predict corel: %.3f' % (predict_corel)

    score = clf.score(X, Y)
    print >> sys.stderr, 'Score = %.3f' % score





