#!/usr/bin/env python
#coding:utf-8
import sys
import log_parser

def parser():
    ml=log_parser.MergeLog_Protobuf()
    line_count=0
    while True:
        line_count+=1
#        if line_count>10:
#            break
        try:
            flag=ml.readNext()
        except Exception,e:#单行解析错误，或单行数据太大
            continue
        if flag <= 0:#0文件结束，-1文件格式错误
            break
        for ms in ml.attr('missions'):
            print 'session里有几个goal:',len(ms.attr('goals'))
        
        for se in ml.attr('searches'):
            print 'ip:',se.attr('ip')
            print 'query:',se.attr('query_info.query') #支持路径查询，attr('query_info.query')=attr('query_info').attr('query')
            for url in se.attr('urls_info'):
                if url.attr('source') == 'SP':
                    print 'aladin srcid:',url.attr('url_info.srcid') #获取SP_Info内数据的方式
                    if url.attr('url_index') != None:
                        print 'aladin url:',se.attr('urls_list')[url.attr('url_index')].attr('url') #获取所有阿拉丁的url的方式
            for act in se.attr('actions_info'):
                if act.attr('index') != None:
                    print '点击结果类型:',se.attr('urls_info')[act.attr('index')].attr('source') #从点击结果的属性
                    print '点击url:',se.getClickMainUrl(act) #封装好的函数，获取某点击的url
            

if __name__=='__main__':
    line_count=parser()
    
