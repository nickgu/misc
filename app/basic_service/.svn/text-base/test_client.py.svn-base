#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import socket
import time
import basic_service

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 8769
    name = None
    find_port = False
    for arg in sys.argv[1:]:
        if arg.find('-i')==0:
            ip = arg.replace('-i', '')
        if arg.find('-p')==0:
            port = int(arg.replace('-p', ''))
            find_port = True
        if arg.find('-n')==0:
            name = arg[2:]

    if not find_port:
        sys.stderr.write('Not port, set to name service\n')

    if name is None:
        sys.stderr.write('connect to %s:%d\n' % (ip, port))
    else:
        sys.stderr.write('connect to name: %s:%s\n' % (ip, name))
    while 1:
        data = raw_input()
        data = data.strip('\n')

        begin = time.time()
        if name:
            ret = basic_service.simple_query_by_name(data, name, ip)
        else:
            ret = basic_service.simple_query(data, ip, port)

        during = time.time() - begin
        print ret
        sys.stderr.write('[tm]=%.3f\n' % during)
