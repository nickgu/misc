#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import ConfigParser
import sys

def list_slice(main_list, idx_list, missing=''):
    out = []
    for idx in idx_list:
        if idx > len(main_list):
            out.append(missing)
        else:
            out.append(main_list[idx])
    return out

class LabelValue:
    def __init__(self, key, value, misc, need_recall):
        self.key = key
        self.value = value
        self.misc = misc
        self.need_recall = need_recall

class DataConf:
    def __init__(self, conffile):
        conf = ConfigParser.ConfigParser()
        conf.read(conffile)
        sec = 'meta'
        conf_key = conf.get(sec, 'key')
        conf_value = conf.get(sec, 'value')
        conf_misc = conf.get(sec, 'misc')
        self.__recall_index = None
        if conf.has_option(sec, 'recall'):
            self.__recall_index = conf.getint(sec, 'recall')

        self.__key_indice = self.__get_indice(conf_key)
        self.__value_indice = self.__get_indice(conf_value)
        self.__misc_indice = self.__get_indice(conf_misc)

    def __get_indice(self, str):
        r = []
        for s in str.split(','):
            if len(s)==0: continue
            if '-' in s:
                u = s.split('-')
                if len(u)!=2: continue
                r.append(int(u[0]))
                r.append(int(u[1]))
            else:
                r.append(int(s))
        return r

    def parse(self, line):
        arr = line.strip('\n').split('\t')
        key = '\t'.join(list_slice(arr, self.__key_indice))
        value = '\t'.join(list_slice(arr, self.__value_indice))
        misc = '\t'.join(list_slice(arr, self.__misc_indice))
        need_recall = False
        if self.__recall_index is not None:
            need_recall = int(arr[self.__recall_index])
        return LabelValue(key, value, misc, need_recall) 

class Evaluation:
    def __init__(self, label_conf, predict_conf):
        self.__labeled = {}
        self.__recall_set = set()
        self.__label_conf = DataConf(label_conf)
        self.__predict_conf = DataConf(predict_conf)

    def load_label(self, label_filename):
        for line in file(label_filename).readlines():
            ldata = self.__label_conf.parse(line)
            if ldata.key not in self.__labeled:
                self.__labeled[ldata.key] = []
            self.__labeled[ldata.key].append( ldata )
            if ldata.need_recall:
                self.__recall_set.add(ldata.key)

    def evaluate(self, predict_output_filename, missing_filename):
        f = file(predict_output_filename)
        
        # stat:
        count_recall = 0
        count_right = 0
        count_right_need_recall = 0

        wrong_dct = {}
        right_dct = {}
        for line in f.readlines():
            ldata = self.__predict_conf.parse(line)
            if ldata.key not in self.__labeled:
                continue
            
            # print 'KEY=[%s] VALUE=[%s] ans=[%s]' % (ldata.key, ldata.value, self.__labeled[ldata.key][0].value)
            count_recall += 1
            for ans in self.__labeled[ldata.key]:
                if ans.value == ldata.value:
                    right = True
                    break
            if right:
                count_right += 1
                if ldata.key in self.__recall_set:
                    count_right_need_recall += 1
                    right_dct[ldata.key] = ldata
            else:
                if ldata.key in self.__recall_set:
                    wrong_dct[ldata.key] = ldata

        # generate reports.
        precise = 0.0
        if count_recall>0: precise = count_right * 100.0 / count_recall
        recall = 0.0
        if len(self.__recall_set)>0: recall = count_right_need_recall * 100.0 / len(self.__recall_set)

        sys.stderr.write('================  REPORT ===============\n')
        sys.stderr.write('Records in data         : %d\n' % count_recall)
        sys.stderr.write('Records right           : %d\n' % count_right)
        sys.stderr.write('Precise                 : %.2f%%\n' % precise)
        sys.stderr.write('Records in need recall  : %d\n' % count_right_need_recall)
        sys.stderr.write('Recall                  : %.2f%%\n' % recall)

        # output missing data.
        missing_file = file(missing_filename, 'w')
        for key in self.__recall_set:
            if key not in right_dct:
                if key not in wrong_dct:
                    missing_file.write('%s\n' % key)
                else: 
                    ldata = wrong_dct[key]
                    missing_file.write('%s\t%s\t%s\n' % (ldata.key, ldata.value, ldata.misc))

if __name__=='__main__':
    from zxdb.arg import *
    arg = Arg()
    arg.str_opt('label_conf', 'b', 'label meta conf')
    arg.str_opt('predict_conf', 'p', 'predict meta conf')
    arg.str_opt('label_data', 'd', 'label data')
    arg.str_opt('predict_data', 'i', 'predict data')
    arg.str_opt('missing_output', 'm', 'missing output')
    opt = arg.init_arg()

    eva = Evaluation(opt.label_conf, opt.predict_conf)
    eva.load_label(opt.label_data)
    eva.evaluate(opt.predict_data, opt.missing_output)
    








