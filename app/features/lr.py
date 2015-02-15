#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#   v1  : lr+corel+data_reader.
#
#
import sys
import math
from sklearn import linear_model

class ConcreteMaker:
    def __init__(self, X=[]):
        self.__X = sorted(X)
    def value(self, value):
        beg = 0
        end = len(self.__X)
        while beg<end:
            mid = (beg + end) / 2
            if self.__X[mid] <= value:
                beg = mid + 1
            else:
                end = mid
        return beg * 1.0 / len(self.__X)

    def dump(self, fn):
        file(fn,'w').write('\n'.join(map(lambda x:str(x), self.__X)))

    def load(self, fn):
        print >> sys.stderr, 'Load concrete file: %s' % (fn)
        self.__X = map(lambda x:float(x.strip('\n')), file(fn).readlines())
        print >> sys.stderr, '%d concrete value loaded.' % len(self.__X)

class LRDataReader:
    def __init__(self, ignore_column=[]):
        self.__ignore_field=set()
        for i in ignore_column:
            self.__ignore_field.add(i)
        self.__FIELD_SEPERATOR = '\t'
        self.__X = []
        self.__Y = []
        self.__key_idx_table = {}
        self.__idx_key_table = []
        self.__not_finalized = True
        self.__use_feature_set = None
        self.__use_idx_set = None

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
        ret_obj = {}
        for col_idx, info in enumerate(arr[1:]):
            if col_idx in self.__ignore_field:
                continue
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
            ret_obj[key] = value
            data.append( (key_idx, value) )
        self.__X.append(data)
        return ret_obj

    def add_feature(self, feature_dct):
        data = self.__X[-1]
        for key, value in feature_dct.iteritems():
            # add 'E_'.
            key = 'E_%s' % key
            key_idx = self.__get_key_idx(key)
            data.append( (key_idx, value) )

    def X(self, concrete=False, use_feature_set=None, no_concrete_set=[], only_concrete=False, dump_concrete_dir=None): 
        if self.__not_finalized:
            self.finalize(concrete, use_feature_set, no_concrete_set, only_concrete, dump_concrete_dir)
        return self.__X
    def Y(self):
        return self.__Y

    def finalize(self, concrete, use_feature_set, no_concrete_set, only_concrete, dump_concrete_dir):
        X = []
        dim = max(self.__key_idx_table.values()) + 1

        no_concrete_set = set(no_concrete_set)
        self.__use_feature_set = use_feature_set
        self.__use_idx_set = set(range(dim))
        if self.__use_feature_set is not None:
            self.__use_idx_set = set()
            for key in self.__use_feature_set:
                idx = self.key2idx(key)
                if idx >= 0:
                    self.__use_idx_set.add(idx)
        print >> sys.stderr, 'dim=%d' % dim
        for x in self.__X:
            d = [0.0] * dim 
            for idx, val in x:
                if idx not in self.__use_idx_set:
                    continue
                d[idx] = val
            X.append(d)
        self.__X = X
        print >> sys.stderr, 'make vector over.'
 
        self.__idx_key_table = [''] * dim
        for key, value in self.__key_idx_table.iteritems():
            self.__idx_key_table[value] = key

        if concrete:
            for use_idx in self.__use_idx_set:
                fname = self.idx2key(use_idx)
                if no_concrete_set and fname in no_concrete_set:
                    continue
                cm = ConcreteMaker(map(lambda x:x[use_idx], self.__X))
                self.__idx_key_table.append( '%s.concrete'% (fname) )
                if dump_concrete_dir:
                    cm.dump(dump_concrete_dir + '/' + fname + '.concrete')
                for i in range(len(self.__X)):
                    self.__X[i].append(cm.value(self.__X[i][use_idx]))
        if only_concrete:
            for d in range(dim):
                for i in range(len(self.__X)):
                    self.__X[i][d] = 0.0
           
        for i in range(dim):
            if i not in self.__use_idx_set:
                continue
            dim_X = map(lambda x:x[i], X)
            corel = self.calc_corel(dim_X, self.__Y, except_zero=True)
            auc = self.AUC(dim_X, self.__Y, except_zero=True)
            print '%d\t%s\tcorel=%.3f\tauc=%.3f' % (i, self.__idx_key_table[i], corel, auc)
        # concrete feature.
        if concrete:
            for i in range(dim, len(self.__X[0])):
                fname = self.__idx_key_table[i]
                if no_concrete_set and fname in no_concrete_set:
                    continue
                dim_X = map(lambda x:x[i], self.__X)
                corel = self.calc_corel(dim_X, self.__Y)
                auc = self.AUC(dim_X, self.__Y)
                print '%d\t%s\tcorel=%.3f\tauc=%.3f' % (i, fname, corel, auc)
        self.__not_finalized = False

    def calc_corel(self, X, Y, except_zero=False):
        if except_zero:
            z_xy = filter(lambda x:x[0]>0, zip(X, Y))
            return self.calc_corel(map(lambda x:x[0], z_xy), map(lambda x:x[1], z_xy))

        avg_X = sum(X) / len(X)
        avg_Y = sum(Y) / len(Y)
        tX = map(lambda x:x-avg_X, X)
        tY = map(lambda y:y-avg_Y, Y)
        up = sum( map(lambda x:x[0]*x[1], zip(tX, tY)) )
        if up == 0.0:
            return up
        corel = up / (math.sqrt(sum(map(lambda x:x*x, tX))) * math.sqrt(sum(map(lambda y:y*y, tY))))
        return corel

    def idx2key(self, idx):
        return self.__idx_key_table[idx]
    def key2idx(self, key):
        return self.__key_idx_table.get(key, -1)

    def AUC(self, predict_Y, Y, output_detail=False, except_zero=False):
        if except_zero:
            z_xy = filter(lambda x:x[0]>0, zip(predict_Y, Y))
            return self.AUC(map(lambda x:x[0], z_xy), map(lambda x:x[1], z_xy))

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
        for idx, (py, y) in enumerate(zip_arr):
            if y == 1: # positive.
                cur_pos_count += 1
            else:
                if idx == len(zip_arr)-1 or zip_arr[idx+1][0] != py:
                    if output_detail:
                        FPR = negative_count * 1.0 / (all_count - all_positive_count)
                        TPR = (positive_count + cur_pos_count) * 1.0 / all_positive_count
                        if int(FPR * 20) > out_cur:
                            for i in range(out_cur, int(FPR*20)):
                                ratio = (i - out_cur + 1.0) / (int(FPR*20) - out_cur)
                                print >> sys.stderr, '%.4f\t%.2f\t%.3f' % (py, i/20.0, (positive_count + cur_pos_count * ratio) * 1.0 / all_positive_count)
                            out_cur = int(FPR*20)

                    inc = ((positive_count + 0.5 * cur_pos_count) / all_positive_count) * stat_count
                    area += inc
                    stat_count = 0
                    positive_count += cur_pos_count
                    cur_pos_count = 0
                stat_count += 1
                negative_count += 1

        return area / negative_count

if __name__=='__main__':
    file_name = '/dev/stdin'
    if len(sys.argv)>1:
        file_name = sys.argv[1]
    print >> sys.stderr, 'FILE_NAME: %s' % file_name

    clf = linear_model.LinearRegression()
    fd = file(file_name)
    reader = LRDataReader()
    line_count = 0
    bad_line_count = 0
    while 1:
        line = fd.readline()
        if line == '':
            break
        try:
            reader.read(line)
        except Exception, e:
            bad_line_count += 1
            continue

        line_count += 1
        if line_count % 100000 == 0:
            print >> sys.stderr, 'Load %d line(s)' % line_count

    print >> sys.stderr, 'bad_line_count : %d' % bad_line_count
    X = reader.X(concrete=True, only_concrete=True, dump_concrete_dir='./intention.concrete')
    Y = reader.Y()
    print >> sys.stderr, 'Read over. len=[%d]' % len(X)

    train_X = map(lambda x:x[1], filter(lambda x:x[0]%10!=0, enumerate(X)))
    train_Y = map(lambda x:x[1], filter(lambda x:x[0]%10!=0, enumerate(Y)))
    #test_X = map(lambda x:x[1], filter(lambda x:x[0]%10==0, enumerate(X)))
    #test_Y = map(lambda x:x[1], filter(lambda x:x[0]%10==0, enumerate(Y)))
    test_X = X[-329:]
    test_Y = Y[-329:]

    clf.fit(train_X, train_Y)
    print >> sys.stderr, 'Trainning over.'
    print >> sys.stderr, 'COEF: %s' % ', '.join(map(lambda x:'%.5f' % x, clf.coef_))
    print >> sys.stderr, 'CONST: %f' % clf.intercept_

    predict_Y = map(lambda f:clf.intercept_+sum(map(lambda x:x[0]*x[1], zip(clf.coef_, f))), test_X)
    predict_corel = reader.calc_corel(test_Y, predict_Y)
    print >> sys.stderr, 'Predict corel: %.3f' % (predict_corel)

    output_file = file('lr_output', 'w')
    for y_a, y_b in zip(test_Y, predict_Y):
        output_file.write('%f\t%f\n' % (y_a, y_b))

    auc = reader.AUC(predict_Y, test_Y, output_detail = True)
    print >> sys.stderr, 'AUC: %.3f' % (auc)

    score = clf.score(test_X, test_Y)
    print >> sys.stderr, 'Score = %.3f' % score





