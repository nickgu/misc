# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import c_prod
import time
import random

def test():
    a=[]
    b=[]
    for i in range(random.randint(100, 200)):
        a.append([i, random.random()])
        b.append([i, random.random()])
    r = c_prod.dot_1d(a, b)
    print r

def test_2d():
    a=[]
    for i in range(random.randint(100, 200)):
        v = []
        for j in range(random.randint(100, 300)):
            v.append( [j, random.random()] )
        a.append(v)
    r = c_prod.self_dot(a)
    print r

if __name__ == '__main__':
    while 1:
        #test()
        test_2d()
        time.sleep(0.5)
