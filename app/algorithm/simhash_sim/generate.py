#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import random
import sys

if __name__=='__main__':
    num = int(sys.argv[1])
    for cnt in range(num):
        x = random.randint(0, 2**32 - 1)
        y = random.randint(0, 2**32 - 1)
        print x, y
