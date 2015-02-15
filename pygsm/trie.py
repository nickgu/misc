#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import logging

class TrieNode:
    def __init__(self, ch):
        self.__jump = {}
        self.__char = ch
        # point to self.
        self.__back = self
        # property info.
        self.__subs_info = []
        self.__is_end = False

    def __str__(self):
        return '<<%s:jlen=%d:bck=%s>>' % (id(self)%10000,len(self.__jump),id(self.__back)%10000)

    def can_jump(self, ch):
        return (ch in self.__jump)

    def jump(self, ch):
        if ch in self.__jump:
            return self.__jump[ch]
        if self == self.__back:
            return self
        return self.__back.jump(ch)

    def add_jump(self, ch):
        n = TrieNode(ch)
        self.__jump[ ch ] = n

    def fill_bfs(self, bfs):
        for ch, node in self.__jump.iteritems():
            bfs.append( (self, ch, node) )

    def build_tree(self):
        ''' make suffix.
        '''
        bfs = [ (None, None, self) ]
        for father, ch, son in bfs:
            son.fill_bfs(bfs)
        for father, ch, son in bfs:
            if father==None: continue
            # root.
            if father.back()==father:
                son.set_back(father)
            else:
                b = father.back().jump(ch)
                son.set_back( b )
        logging.info('TrieNode: %d' % len(bfs))
        '''
        for father, ch, son in bfs:
            print repr(ch), son
        '''

    def set_back(self, back):
        self.__back = back
        if back.is_end():
            self.__is_end = True
    def end(self, s, info=None):
        self.__is_end = True
        self.__subs_info.append( (s, info) )

    def ch(self): return self.__char
    def subs_info(self): return self.__subs_info
    def end_here_info(self):
        if self.__back==None or self.__back==self:
            return self.__subs_info
        else:
            return self.__subs_info + self.__back.end_here_info()
    def is_end(self): return self.__is_end
    def back(self): return self.__back

class Trie:
    '''
        Example:
            
            # make dict.
            dct = trie.Trie()
            for lemma in some_list:
                dct.insert(lemma)
            dct.end_insert() // VERY VERY IMPORTANT


            # how to search.
            for begin_pos, term, info in dct.find(text):
                # do something.
    '''

    def __init__(self):
        self.__root = TrieNode(None)

    def insert(self, s, info=None):
        ''' 插入一个字符串, 或者一个值
        '''
        cur = self.__root
        for ch in s:
            if not cur.can_jump(ch):
                cur.add_jump(ch)
            cur = cur.jump(ch)
        cur.end(s, info)

    def end_insert(self):
        self.__root.build_tree()
    
    def find(self, text):
        ''' 查找所有存在于字符串内的信息
        返回形式： [ (pos, s1, info1), (pos, s2, info2) ]
        '''
        cur = self.__root
        pos = 0
        for ch in text:
            cur = cur.jump(ch)
            #print '%s] [%s] [%s] [%d] b=%s' % (repr(ch), cur.ch(), id(cur), cur.is_end(), id(cur.back()))
            if cur.is_end():
                for subs, info in cur.end_here_info():
                    yield (pos - len(subs) + 1, subs, info)
            pos += 1

if __name__=='__main__':
    from zxdb.tool import *
    from zxdb.arg import *

    arg = Arg()
    arg.str_opt('input', 'i', '输入模式信息', required=True)
    arg.str_opt('text', 't', '输入文本信息', required=True)
    opt = arg.init_arg()
    
    trie = Trie()
    f = file(opt.input)
    for kv in map(lambda x:x.strip('\n').split('\t'), f.readlines()):
        if len(kv)==1:
            trie.insert(kv[0], None)
        else:
            trie.insert(kv[0], kv[1])
    trie.end_insert()

    text = ''.join(file(opt.text).readlines())
    for pos, s, info in trie.find(text):
        print '%s\t%s\t%s' % (pos, s, info)
    




