#! /bin/env python
# encoding=utf-8
#   nickgu
# 

import json
import sys

class JsonTreeView:
    def __init__(self, file_name):
        self.__objs = []
        self.__cur = self.__objs
        self.__path = []
        for line in file(file_name).readlines():
            d = json.loads(line.strip('\n'))
            self.__objs.append( d )
        print 'Load json over (%d objects loaded)' % len(self.__objs)

    def ls(self):
        if isinstance(self.__cur, list):
            print '<list:%d>' % len(self.__cur)
        elif isinstance(self.__cur, dict):
            for key in self.__cur:
                print key.encode('utf-8')
        else:
            print self.__cur

    def cd(self, path):
        p = path.split('/')
        if p[0] == '':
            self.__path = []
            self.__cur = self.__objs
        for item in p:
            if item == '':
                continue
            elif item == '.':
                continue
            elif item == '..':
                self.__cur = self.__path.pop()
            else: # downward.
                self.__path.append(self.__cur)
                if isinstance(self.__cur, list):
                    self.__cur = self.__cur[int(item)]
                elif isinstance(self.__cur, dict):
                    self.__cur = self.__cur[item]

    def pwd(self):
        print ''

    def dump(self):
        print json.dumps(self.__cur, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    to = JsonTreeView(sys.argv[1])
    while 1:
        sys.stdout.write('> ')  # prompt.
        cmd = sys.stdin.readline().strip('\n').strip(' ')
        cmds = cmd.split(' ')
        if cmds[0] == 'ls':
            to.ls()
        elif cmds[0] == 'cd':
            to.cd(cmds[1])
        elif cmds[0] == 'pwd':
            to.pwd()
        elif cmds[0] == 'dump':
            to.dump()
