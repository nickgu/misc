#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import json
import sys

__VERSION__='1.0.0'

class JsonQ:
    def __init__(self, obj, query):
        self.__cur_path = []
        self.__answers = []
        self.__key = None
        self.__parse_query(query)
        self.__iter(obj) 

    def answers(self): 
        return self.__answers

    def __parse_query(self, query):
        '''
            query format:
                word : key
        '''
        self.__key = query

    def __match(self, obj):
        if (len(self.__cur_path)>0 
            and self.__cur_path[len(self.__cur_path)-1] == self.__key):
            return True
        return False

    def __iter(self, obj):
        if self.__match(obj):
            self.__answers.append(obj)

        if isinstance(obj, list):
            for item in obj:
                self.__iter(item)
        elif isinstance(obj, dict):
            for key, value in obj.iteritems():
                self.__cur_path.append(key)
                self.__iter(value)
                self.__cur_path.pop()


def jsonq(obj, query):
    seeker = JsonQ(obj, query)
    for x in seeker.answers():
        yield x

class JsonFormater:
    def __init__(self):
        self.__init_iter()

    def __init_iter(self):
        self.__text = ''
        self.__stack = -1

    def check(self, obj):
        self.__init_iter()
        self.__iter(obj)
        return self.__text

    def __iter(self, obj):
        self.__stack += 1
        if isinstance(obj, list):
            self.__append( 'LIST:%d [\n' % len(obj) )
            for item in obj:
                self.__iter(item)
            self.__append( ']\n' )
        elif isinstance(obj, dict):
            self.__append( 'DICT:%d {\n' % len(obj) )
            for key, value in obj.iteritems():
                self.__append('\'%s\': \n' % key)
                self.__iter(value)
            self.__append( '}\n' )
        else:
            self.__append( '%s\n' % type(obj))
        self.__stack -= 1

    def __append(self, text, offset=0):
        self.__text += '%s%s' % ('  ' * (self.__stack + offset), text)


if __name__=='__main__':
    if len(sys.argv)==1:
        # output each format.
        formater = JsonFormater()
        while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            obj = json.loads(line)
            print formater.check(obj)
            # only output first one.
            break
    elif (sys.argv[1]=='-h' 
            or sys.argv[1]=='--help'
            or sys.argv[1]=='-H'):
        print >> sys.stderr, '''VERSION : %s
Usage:
    1. jsonq.py [<query>]  : output selector.
    2. jsonq.py            : output format of first object.


''' % __VERSION__
    else:
        # execute jsonQuery
        query = sys.argv[1]
        while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            obj = json.loads(line)
            for x in jsonq(obj, query):
                print x



