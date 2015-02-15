#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import traceback
import socket
import sys
import time

HEADER_LENGTH = 8
DETECTIVE_MSG = 'Are_you_alive?'

def echo(input_text):
    return ('ACK: ' + input_text)

def sock_recv(sock):
    d = sock.recv(HEADER_LENGTH)
    if len(d)==0:
        return None
    data_len = int(d)
    #print data_len
    data = ''
    while 1:
        n = min(4096, data_len)
        d = sock.recv(n)
        if not d:
            break

        data_len -= len(d)
        data += d

        #print 'left=%d cur=%d' % (data_len, len(data))
        if data_len<=0:
            break
    return data

def sock_send(sock, data):
    data_len = '%8d' % len(data)
    sock.sendall(data_len)
    sock.sendall(data)

def simple_query(query, ip='127.0.0.1', port=12345):
    sys.stderr.write('SEEK_TO: %s:%s\n' % (ip, port))
    clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clisock.connect((ip, port))

    sock_send(clisock, query)
    ret = sock_recv(clisock)
    clisock.close()
    return ret

def detect(ip='127.0.0.1', port=12345):
    try:
        ret = simple_query(DETECTIVE_MSG, ip, port)
        if ret != 'YES':
            return False
    except Exception, msg:
        sys.stderr.write('detect err: %s\n' % msg)
        return False
    return True

def simple_query_by_name(query, name, ip='127.0.0.1'):
    cmd = 'SEEK\t%s' % name
    ret = simple_query(cmd, ip, port=8769)
    arr = ret.split('\t')
    if arr[0] != 'OK':
        sys.stderr.write('seek name failed! [%s]' % ret)
        return None
    port = int(arr[1])
    return simple_query(query, ip, port)

class BasicService:

    def __init__(self):
        self.__handler_init = None
        self.__handler_process = None
        self.__handler_timer_process = None
        self.__timer = 0.0

    def set_init(self, h_init):
        self.__handler_init = h_init

    def set_process(self, h_process):
        self.__handler_process = h_process

    def set_timer_deamon(self, h_process, seconds=60.0):
        '''
            set a process which will be called each time interval.
        '''
        self.__handler_timer_process = h_process
        self.__timer = seconds

    def run_with_name(self, name, desc='No description.', ip='127.0.0.1', port=12345):
        '''
            尝试和本机服务管理器建立映射关系
        '''
        cmd = 'REGEDIT\t%s\t%d\t%s' % (name, port, desc)
        ret = simple_query(cmd, ip, port=8769)
        arr = ret.split('\t')
        if arr[0] != 'OK': 
            sys.stderr.write('SET NAME FAILED! [%s]' % ret)
            return
        self.run(ip, port)
        
    def run(self, ip='127.0.0.1', port=12345):
        if self.__handler_init:
            sys.stderr.write('init..\n')
            self.__handler_init()

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
        self.__sock.bind( (ip, port) )
        self.__sock.listen(32)
        sys.stderr.write('listen : %s:%d\n' % (ip, port))

        last_time = time.time()
        
        try:
            while 1:
                # check time at first.
                if self.__handler_timer_process:
                    dt = time.time() - last_time
                    if dt >= self.__timer:
                        try:
                            self.__handler_timer_process()
                        except Exception, msg:
                            sys.stderr.write('error in time_handler: %s\n' % msg)
                        last_time = time.time()

                # set a timer for accept:
                #   because i need to run a timer process.
                self.__sock.settimeout(1);
                try:
                    clisock, (remote_host, remote_port) = self.__sock.accept()
                except socket.timeout, msg:
                    continue

                try:
                    data = sock_recv(clisock)
                    if data == DETECTIVE_MSG:
                        sock_send(clisock, 'YES')
                    else:
                        sys.stderr.write('[%s:%s] connected dl=%d\n' % (remote_host, remote_port, len(data)))
                        if self.__handler_process:
                            response = self.__handler_process(data)
                            if response:
                                sock_send(clisock, response)

                except Exception, msg:
                    sys.stderr.write('err [%s]!\n' % msg)
                    traceback.print_stack()
                    traceback.print_exc()
                    continue
                finally:
                    clisock.close()
        finally:
            sys.stderr.write('byebye.\n')
            self.__sock.close()

class ManagerService:
    def __init__(self):
        self.__name_dct = {}
        self.__desc_dct = {}
        self.__recover()
        self.__svr = BasicService()
        self.__svr.set_process(self.process)
        self.__svr.set_timer_deamon(self.deamon_process, 5)

    def run(self):
        self.__svr.run(port=8769)

    def deamon_process(self):
        '''
            check whether each service is alive.
        '''
        sys.stderr.write('detect: %s\n' % time.asctime()) 
        del_names = []
        for name, port in self.__name_dct.iteritems():
            alive = detect(port=port)
            if not alive:
                sys.stderr.write('%s : %s[%d] is dead.\n' % (time.asctime(), name, port))
                del_names.append(name)
        for name in del_names:
            del self.__name_dct[name]
            del self.__desc_dct[name]
        self.__backup()

    def process(self, cmd):
        '''
            3 type(s) of cmd:
                'SEEK[\t][name]' => 'OK\tPORT' or 'ERR\tNOT_FOUND'
                'REGEDIT[\t][name][\t][port][\t][desc]' => 'OK' or 'ERR\tmsg'
                'INFO' => 'OK\tname info.'
        '''
        cmd = cmd.replace('\n', '')
        cmd = cmd.replace('###', '')
        cmd = cmd.replace('||', '')
        arr = cmd.split('\t')
        if arr[0] == 'SEEK':
            if len(arr)!=2:
                return 'ERR\tpara_num=%d' % len(arr)
            name = arr[1]
            if name not in self.__name_dct:
                return 'ERR\tNOT_FOUND'
            return 'OK\t%d' % self.__name_dct[name] 
        elif arr[0] == 'REGEDIT':
            if len(arr)!=4:
                return 'ERR\tpara_num=%d' % len(arr)
            name, port, desc = arr[1:4]
            if ':' in name:
                return 'ERR\tINVALID_NAME_NO_:_'
            port = int(port)
            self.__name_dct[name] = port
            self.__desc_dct[name] = desc
            return 'OK'
        elif arr[0] == 'INFO':
            info = ''
            for name, port in self.__name_dct.iteritems():
                desc = self.__desc_dct.get(name, '')
                info += '%s||%s||%s###' % (name, port, desc)
            return 'OK\t%s' % info
    
    def __recover(self):
        try:
            f = file('service_info.txt')
        except:
            sys.stderr.write('no backup info.\n')
            return
        for l in f.readlines():
            arr = l.strip('\n').split('\t')
            if len(arr)!=3: 
                continue
            name, port, desc = arr
            port = int(port)
            if name not in self.__name_dct:
                self.__name_dct[name] = port
                self.__desc_dct[name] = desc

    def __backup(self):
        f = file('service_info.txt', 'w')
        for name, port in self.__name_dct.iteritems():
            desc = ''
            if name in self.__desc_dct:
                desc = self.__desc_dct[name]
            f.write('%s\t%d\t%s\n' % (name, port, name))
        f.close()

if __name__=='__main__':
    # test a svr.
    svr = BasicService()
    svr.set_process(echo)
    svr.run_with_name('ECHO', desc='This is a echo service.')





