#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import simhash_sim
import pygsm.basic_service as bs

seeker = simhash_sim.SimHash_Seeker(sys.argv[1])
def process(query):
    sign1, sign2 = query.strip('\n').split('\t')
    sign1 = int(sign1)
    sign2 = int(sign2)
    return seeker.query(sign1, sign2)

if __name__=='__main__':
    svr = bs.BasicService()
    svr.set_process(process)
    svr.run(port=54355)

