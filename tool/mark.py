#! /usr/local/bin/python
# encoding=utf-8
# author: nickgu 
# 

import sys

if __name__=='__main__':
    bookmarks_filename = '/Users/nickgu/bookmarks'

    if sys.argv[1] == '-c':
        # clear all.
        print >> file(bookmarks_filename, 'w'), ''

    elif sys.argv[1] == '-l':
        # list all.
        for line in file(bookmarks_filename).readlines():
            print line.strip()

    elif sys.argv[1] == '-s':
        query = sys.argv[2]
        print >> sys.stderr, 'Search [%s]' % query
        # search mode.
        for line in file(bookmarks_filename).readlines():
            if query in line:
                print line.strip()

    else:
        print >> file(bookmarks_filename, 'a'), '\t'.join(sys.argv[1:])
        print >> sys.stderr, 'mark ok'

