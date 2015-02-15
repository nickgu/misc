#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import os
import re
import sys

class Ulpack_KVDict(object):
    '''
        a dummy class.
    '''
    def __init__(self): 
        pass

class ULPackage(object):
    '''
        an ul-package.
        pack.kv : kv info, such as pack.kv.Url
        pack.dict : get a readonly dict.
        pack.title
        pack.cont
        pack.page
        pack.body
    '''
    def __init__(self, text):
        self.kv = Ulpack_KVDict()
        self.__kvdict = {}
        self.__body = None

        kv_list = text.split('\n')
        body_begin = -1
        line_id = 0
        for kvs in kv_list:
            if kvs == '\r':
                body_begin = line_id
                break
            line_id += 1
            kvs = kvs.strip()
            try:
                k, v = kvs.split(' : ')[0:2]
                # this statment cost a lot of time.
                #k = re.subn('^.*\x00', '', k)[0]
            except Exception, msg:
                continue
            self.__kvdict[k] = v
        self.kv.__dict__ = self.__kvdict

        kv_list[-1] = kv_list[-1].replace('~EOF!', '')
        self.__body = ''.join(kv_list[body_begin : len(kv_list)])
        self.__body = self.__body.replace('\t', '')
        self.__body = self.__body.replace('\n', '')
        self.__parse_body()

    @property
    def cont(self): return self.__cont
    @property
    def title(self): return self.__title
    @property
    def page(self): return self.__page
    @property
    def body(self): return self.__body
    @property
    def dict(self): return self.__kvdict

    def debug(self):
        print '--- DEBUG_ULPACK ---'
        for k, v in self.iteritems():
            print '%s :: %s' % (k, v)
        print len(self.__body)

    def __parse_body(self):
        try:
            self.__cont = None
            self.__title = None
            self.__page = None

            body = self.body
            info = self.kv.Body
            segments = []
            beg = 0
            x = info.split('+')
            for s in x:
                seg, length = re.match('([A-Z]*)([0-9]*)', s).groups()
                length = int(length)
                if seg=='CONT':
                    self.__cont = body[beg:beg+length]
                elif seg=='TITL':
                    self.__title = body[beg:beg+length]
                elif seg=='PAGE':
                    self.__page = body[beg:beg+length]
        except Exception, msg:
            sys.stderr.write('Exception: %s\n' % msg)
            return 

class ULPackReader(object):
    SEPERATOR = '~EOF!~BUF!'
    def __init__(self, stream=sys.stdin):
        self.__stream = stream
        self.__package = ''

    def read(self):
        url = ''
        while 1:
            l = self.__stream.readline()
            if l == '': break
            if ULPackReader.SEPERATOR in l:
                info = l.split(ULPackReader.SEPERATOR)
                self.__package += info[0]
                yield ULPackage(self.__package)
                self.__package = info[1]
            else:
                self.__package += l
        if self.__package != '':
            yield ULPackage(self.__package)


def deal_text(text):
    if text is None:
        return ''
    return ' '.join( text.replace('\t', '').split('\n') )

if __name__=='__main__':
    reader = ULPackReader(sys.stdin)
    param = set('TITL')
    if len(sys.argv)>0:
        param = set(sys.argv[1].split('+'))
    for pack in reader.read():
        url = pack.kv.Url

        out = []
        if 'URL' in param:
            out.append(url)
        if 'TITL' in param:
            out.append(pack.title)
        if 'CONT' in param:
            out.append(deal_text(pack.cont))
        if 'PAGE' in param:
            out.append(deal_text(pack.page))

        print '\t'.join(map(lambda x:str(x), out))
