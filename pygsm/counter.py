#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#   
#   V1.0.2 change::
#       add Mapper mode. (--mapper)
#
#   V1.0.1 change:: 
#       dump(self, stream, sort)
#
#   V1.0
# 

class MapperCounter:
    def __init__(self):
        self.__dct = {}

    def inc(self, key, inc=1):
        if key not in self.__dct:
            self.__dct[key] = 0
        self.__dct[key] += inc

    def dump(self, stream, sort=False):
        if sort:
            for key, value in sorted(self.__dct.iteritems(), key=lambda x:-x[1]):
                print '%s\t%s' % (key, value)
        else:
            for key, value in self.__dct.iteritems():
                print '%s\t%s' % (key, value)



import sys
if __name__=='__main__':
    output_int = False
    arg_set = set(sys.argv[1:])
    cut_num = 0
    mapper_mode = False
    if '-i' in arg_set:
        # output as integer.
        output_int = True
    if '--mapper' in arg_set:
        mapper_mode = True
    for arg in arg_set:
        if arg.find('-c') == 0:
            cut_num = int(arg[2:])

    if mapper_mode:
        ct = MapperCounter()
        while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            ct.inc(line.strip('\n'))
        ct.dump(sys.stdout)

    else:
        # reducer.
        last_key = None
        acc_value = 0
        while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            arr = line.strip('\n').split('\t')
            if len(arr)!=2:
                continue
            key, value = arr
            if output_int:
                value = int(value)
            else:
                value = float(value)
            if key != last_key:
                if last_key:
                    if acc_value >= cut_num:
                        print '%s\t%s' % (last_key, acc_value)
                last_key = key
                acc_value = 0
            acc_value += value
        if last_key:
            if acc_value >= cut_num:
                print '%s\t%s' % (last_key, acc_value)

