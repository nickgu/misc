# -*- coding: utf-8 -*-
# gusimiu@baidu.com
#   
#   特征读取工具
#   V1.0    完成基本功能
#               reader, auc, corel
#   V1.01   Add expr/test_all function.
#   

import math
import sys

class FMeta:
    def __init__(self):
        self.__current_idx = 0
        self.__key2idx = {}
        self.__idx2key = {}

    def feature_num(self): return self.__current_idx

    def all_keys(self):
        return list(self.__key2idx.keys())

    def add_mapping(self, key, orig_key):
        if orig_key not in self.__key2idx:
            raise 'No original key: [%s]' % orig_key
        self.__key2idx[key] = self.__key2idx[orig_key]
        self.__idx2key[idx].add(key)

    def key(self, key):
        if key not in self.__key2idx:
            self.__key2idx[key] = self.__current_idx
            self.__idx2key[self.__current_idx] = set([key])
            self.__current_idx += 1
        return self.__key2idx.get(key, None)

    def names(self, idx):
        return self.__idx2key.get(idx, [])

    def add_feature(self, x, key, value):
        idx = self.key(key)
        if idx >= len(x):
            x.extend( [0.0] * (idx - len(x) + 1) )
        x[idx] = value

class FAccessor:
    def __init__(self, key=None, meta=None):
        self.__key = key
        self.__meta = meta

    def key(self): return self.__key

    def __call__(self, feature, meta=None, key=None):
        idx = None
        use_meta = self.__meta
        if meta:
            use_meta = meta

        if key is not None:
            idx = use_meta.key(key) 
        elif self.__key is not None:
            idx = use_meta.key(self.__key)
        else:
            raise 'FeatureAccessor no key.'
        return feature[idx]

class FKeyAccessor:
    def __init__(self, x, meta):
        self.__x = x
        self.__f = FAccessor(key=None, meta=meta)
    def __call__(self, key):
        return self.__f(self.__x, key=key)

class FReader:
    def __init__(self, seperator='\t', label_position=0, kv_seperator=None):
        print >> sys.stderr, 'Init Freader. sep:[%s] kvsep:[%s] label_pos:[%d]' % (
                seperator, kv_seperator, label_position)
        self.__seperator = seperator
        self.__label_position = label_position
        self.__kv_seperator = kv_seperator
        self.__extra_info = []

    def extra_info(self): return self.__extra_info

    def read(self, line, meta):
        self.__extra_info = []
        arr = line.strip('\n').split(self.__seperator)
        label = None
        if self.__label_position is not None:
            label = float(arr[self.__label_position])

        f = [0.0] * meta.feature_num()
        for idx, info in enumerate(arr):
            if idx == self.__label_position:
                continue

            k = idx
            v = None
            try:
                if self.__kv_seperator is None:
                    v = float(info)
                else:
                    k, v = info.split(self.__kv_seperator)
                    v = float(v)
            except Exception, e:
                self.__extra_info.append(info)
                continue
            k = meta.key(k)
            if k == len(f):
                f.append( v ) 
            else:
                f[k] = v
        return f, label

    def finalize(self, X, meta):
        for i in range(len(X)):
            if len(X[i]) < meta.feature_num():
                X[i].extend( [0] * (meta.feature_num()-len(X[i]) + 1) )

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

def corel(X, Y, except_zero=False):
    if except_zero:
        z_xy = filter(lambda x:x[0]>0, zip(X, Y))
        return corel(map(lambda x:x[0], z_xy), map(lambda x:x[1], z_xy))

    avg_X = sum(X) / len(X)
    avg_Y = sum(Y) / len(Y)
    tX = map(lambda x:x-avg_X, X)
    tY = map(lambda y:y-avg_Y, Y)
    up = sum( map(lambda x:x[0]*x[1], zip(tX, tY)) )
    if up == 0.0:
        return up
    corel = up / (math.sqrt(sum(map(lambda x:x*x, tX))) * math.sqrt(sum(map(lambda y:y*y, tY))))
    return corel


if __name__ == '__main__':
    import pygsm.arg
    import sys

    def parse_accessor(conf_string, meta):
        ret = []
        if conf_string:
            for key in conf_string.split(','):
                try: 
                    ret.append(FAccessor(int(key), meta=meta))
                except:
                    ret.append(FAccessor(key, meta=meta))
        return ret

    def if_condition(x, y, meta, expr):
        if expr is None:
            return True
        f = FKeyAccessor(x, meta)
        __label__ = y
        return eval(expr)

    args = pygsm.arg.Arg('Feature reader.')
    args.bool_opt('test_all', 'ta', 'test all keys. output AUC/corel between each features and label.')
    args.str_opt('filename', 'f', 'input file', default='/dev/stdin')
    args.str_opt('seperator', 's', 'data seperator, default is [tab]', default='\t')
    args.str_opt('kv_seperator', 'v', 'KeyValue seperator, default is None', default=None)
    args.str_opt('test', 't', 'given keys, output AUC/corel between each features and label.', default=None)
    args.str_opt('expr', 'e', 
            'given an expression. If condition met, output instance. Use F("featurename") or __label__ to access feature or label', default=None)
    args.str_opt('dump_features', 'o',
            'dump feature of keys list(such as \'all\', \'key1,key2\'), output is tab splited(first column is label).', default=None)
    opt = args.init_arg()

    meta = FMeta()
    test_accessors = parse_accessor(opt.test, meta)
    output_accessor = parse_accessor(opt.dump_features, meta)

    reader = FReader(seperator=opt.seperator, kv_seperator=opt.kv_seperator)
    fd = file(opt.filename)
    X = []
    Y = []
    while 1:
        line = fd.readline()
        if line == '':
            break
        f, l = reader.read(line, meta)
        Y.append(l)
        X.append(f)
    print >> sys.stderr, '%d records load, feature_num:%d' % (len(X), meta.feature_num())
    reader.finalize(X, meta)

    new_X = []
    new_Y = []
    if opt.expr:
        for x, y in zip(X, Y):
            if not if_condition(x, y, meta, opt.expr):
                continue
            new_X.append(x)
            new_Y.append(y)
        X = new_X
        Y = new_Y
        print >> sys.stderr, 'after expr[%s], %d records remains' % (opt.expr, len(X))
    
    for accessor in test_accessors:
        x = map(lambda x:accessor(x), X)
        auc = AUC(x, Y)
        cor = corel(x, Y)
        print '%.4f\t%.4f\t%s' % (auc, cor, accessor.key())

    # test all keys.
    if opt.test_all:
        for key in meta.all_keys():
            acc = FAccessor(key, meta=meta)
            x = map(lambda x:acc(x), X)
            auc = AUC(x, Y)
            cor = corel(x, Y)
            print '%.4f\t%.4f\t%s' % (auc, cor, acc.key())

    if len(output_accessor)>0:
        for idx, x in enumerate(X):
            out = []
            out.append(Y[idx])
            for ac in output_accessor:
                out.append(ac(x))
            print '\t'.join(map(lambda x:'%f'%x, out))






