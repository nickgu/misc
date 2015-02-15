#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#   
#   V1.1
#       fix query.decode('ignore')
#

import sys
import os
import urllib
import random

DefaultUser = 'gusimiu'
DefaultDomain='http://dataview.baidu.com/rank/rank'

def DataViewSeek(data_name, query, domain=DefaultDomain):
    '''
        seek for single keys.
    '''
    quri = urllib.quote(query.decode('gb18030', 'ignore').encode('utf-8'))
    ret = os.system('wget "%s/test_bp_ajax_info_json.php?cmd=%s&tid=1&id=1&keyinfo=%s" -O temp.json 2> /dev/null' % 
            (domain, data_name, quri))
    if ret!=0:
        print >> sys.stderr, 'DataViewSeek: seek data failed! [%s]' % ret
        return None
    ret = ''.join( file('temp.json').readlines() )
    #os.system('rm temp.json')
    return ret

def DataViewMultiSeek(data_name, query_list, domain=DefaultDomain):
    '''
        seek for multi-keys.
        return a dct which contain answer text of each key.
    '''
    seed = random.randint(0, 10000)
    key_fn = 'query.%d.txt' % seed
    status_fn = 'status.%d.txt' % seed
    data_fn = 'data.%d.txt' % seed

    ret_dct = {}
    key_file = file(key_fn, 'w')
    for query in query_list:
        print >> key_file, '%s' % query
        ret_dct[query] = ''
    key_file.close()

    hostname = os.popen('hostname').readline().strip('\n')
    pwd = os.popen('pwd').readline().strip('\n')
    ftp_path = ('ftp://%s/%s/%s' % (hostname, pwd, key_fn))
    #print ftp_path
    url = "http://dataview.baidu.com/rank/batchSeek.php?dataname=%s&type=ftp&username=%s&input=%s" % (
            data_name, DefaultUser, urllib.quote(ftp_path).replace('/', '%2F'))
    #print url
    ret = os.system('wget "%s" -O %s 2> /dev/null' % (url, status_fn))
    try:
        if ret!=0:
            print >> sys.stderr, 'DataViewMultiSeek: seek data failed! wget_ret=[%s]' % ret
            raise Exception
        ret_arr = file(status_fn).readline().strip('\n').split('\t')
        if ret_arr[0] != '0' or len(ret_arr)!=2:
            print >> sys.stderr, 'DataViewMultiSeek: seek data failed! return code: %s len=%d' % (ret_arr[0], len(ret_arr))
            raise Exception
        ret_ftp = ret_arr[1]
        os.system('wget "%s" -O %s 2> /dev/null' %  (ret_ftp, data_fn))
        for line in file(data_fn).readlines():
            arr = line.strip('\n').split('\t')
            if len(arr)<=1:
                continue
            key = arr[0]
            data = '\t'.join(arr[1:])
            ret_dct[key] = data
    except Exception, ex:
        print >> sys.stderr, "Exception: %s" % ex
    finally:
        os.system('rm -rf %s %s %s' % (key_fn, status_fn, data_fn))
        return ret_dct

if __name__=='__main__':
    DATA_NAME='MM-QD0331'
    if len(sys.argv)>1:
        DATA_NAME = sys.argv[1]
    print >> sys.stderr, 'DATA_NAME : %s' % DATA_NAME
    while 1:
        line = sys.stdin.readline()
        if line == '':
            break
        query = line.strip('\n')
        data = DataViewSeek(DATA_NAME, query)
        print data
