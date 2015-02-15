#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import os

class SimHash_Seeker:
    def __init__(self, filename):
        # suppose the input file is in asec-order.
        self.__MAX_DIFF = 3
        self.__MAX_BIT = 64
        self.__veclist = []
        fd = file(filename)
        is_sorted = True
        while 1:
            line = fd.readline()
            if line == '':
                break
            arr = line.strip('\n').split(' ')
            if len(arr)!=2:
                continue
            s = (int(arr[0]), int(arr[1]))
            if is_sorted and len(self.__veclist) > 0 and s < self.__veclist[-1]:
                is_sorted = False
                print >> sys.stderr, 'Input file is not sorted!!'
            self.__veclist.append( s )
        if not is_sorted:
            print >> sys.stderr, 'Load file over. len=%d' % len(self.__veclist)
            self.__veclist = sorted(self.__veclist)
            print >> sys.stderr, 'Sort list over.'

    def query(self, sign_A, sign_B):
        self.__temp_ans = []
        self.__dfs( (sign_A, sign_B), 0, len(self.__veclist), 0, 0)
        return self.__temp_ans

    def __dfs(self, sign, vbegin, vend, cur_pos, cost):
        #print '%d:%d pos=%d cost=%d' % (vbegin, vend, cur_pos, cost)
        if vbegin == vend or cost > self.__MAX_DIFF:
            return
        if cur_pos>=self.__MAX_BIT:
            for s in self.__veclist[vbegin : vend]:
                self.__temp_ans.append( s )
            return 
        cur_bit = self.__bit(sign, cur_pos)
        sep = self.__locate_sep(vbegin, vend, cur_pos)
        #print '%d:%d pos=%d cost=%d sep=%d cur_bit=%d' % (vbegin, vend, cur_pos, cost, sep, cur_bit)
        if cur_bit == 0:
            self.__dfs(sign, vbegin, sep, cur_pos + 1, cost)
            self.__dfs(sign, sep, vend,   cur_pos + 1, cost + 1)
        elif cur_bit == 1:
            self.__dfs(sign, vbegin, sep, cur_pos + 1, cost + 1)
            self.__dfs(sign, sep, vend,   cur_pos + 1, cost)

    def __bit(self, sign, pos):
        # get the N'th bit of sign.
        if pos >= 32:
            return (sign[1] / (2 ** (63-pos))) % 2
        else:
            return (sign[0] / (2 ** (31-pos))) % 2

    def __locate_sep(self, begin, end, bitpos):
        # find the first sign which is 1 on bitpos.
        sep = end
        while begin < end:
            mid = (begin + end) / 2
            mb = self.__bit(self.__veclist[mid], bitpos)
            if mb == 1:
                sep = mid
                end = mid
            else: # mb = 0
                begin = mid + 1    
        return sep

if __name__=='__main__':
    seeker = SimHash_Seeker(sys.argv[1])
    print >> sys.stderr, 'init over.'
    while 1:
        line = sys.stdin.readline()
        if line == '':
            break
        arr  = line.strip('\n').split('\t')
        if len(arr)!=2:
            print >> sys.stderr, 'Line error.'
            continue
        out_list = seeker.query(int(arr[0]), int(arr[1]))
        print 'answer num : %d' % len(out_list)
        for s in out_list[:5]:
            print '%d:%d' % (s[0], s[1]) 

