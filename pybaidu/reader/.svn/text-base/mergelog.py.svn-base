#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#
#   V1.0.1:
#       feature:
#           right-recomm disp/click info.
#       fix bug:
#           'query_info.original_query' and 'query_info.query' mismatch.
#       
#   V1.0:
#       complete first version.
#

import sys
import urllib
import log_parser
import base64

class MergeLogRightDisp:
    def __init__(self):
        pass

    def parse(self, right_url):
        try:
            self.display_pos = right_url.attr('display_pos')
            self.src_id = None
            self.title = None
            self.cardmd5 = None
            self.display_num = -1
            self.uri_name_list = []
            uri_list = []
            name_list = []

            einfo = right_url.attr('url_info.externalinfo')
            self.src_id = right_url.attr('url_info.resourid')
            for kv in einfo.split('&'):
                if kv.find('itemuri=')==0:
                    uri_list = filter(lambda x:len(x), kv.replace('itemuri=', '').split('{\\a}'))
                elif kv.find('drsv=')==0:
                    inner_kv_list = kv.replace('drsv=', '').split('{s}')
                    for inner_kv in inner_kv_list:
                        if inner_kv.find('item_disp{e}')==0:
                            iv = int(inner_kv.replace('item_disp{e}', ''))
                            self.display_num = iv
                        if inner_kv.find('item_names{e}')==0:
                            name_list = base64.b64decode(inner_kv.replace('item_names{e}', '')).split('\t')
                elif kv.find('cardmd5=')==0:
                    self.cardmd5 = kv.replace('cardmd5=', '')
                elif kv.find('title=')==0:
                    self.title = urllib.unquote(kv.replace('title=', '')).decode('utf-8', 'ignore').encode('gb18030')
            if len(name_list) == len(uri_list):
                self.uri_name_list = zip(uri_list, name_list)
            elif len(uri_list)==0:
                # uri list is missing.
                self.uri_name_list = [(None, name) for name in name_list]
            elif len(name_list)==0:
                # name is missing.
                self.uri_name_list = [(uri, None) for uri in uri_list]
            else:
                for i in range(max(len(uri_list), len(name_list))):
                    x = None
                    if i<len(uri_list): x=uri_list[i]
                    y = None
                    if i<len(name_list): y=name_list[i]
                    self.uri_name_list.append( (x, y) )

        except Exception,e :
            print 'parse error: %s : %s' % (self.src_id, e)
            return False
        if len(self.uri_name_list) == 0:
            return False
        return True

class MergeLogAction:
    def __init__(self, action, se):
        self.__action = action
        self.act_type = action.attr('fm')
        self.click_url = None
        self.click_type = None
        self.right_click_item_uri = None
        self.right_click_item_name = None

        tp = action.attr('tp')
        if tp:
            self.tp_dct = dict(filter(lambda x:len(x)==2, map(lambda x:x.split('='), tp.split(':'))))

        if action.attr('index') != None:
            self.click_url = se.getClickMainUrl(action)
            self.click_type = se.attr('urls_info')[action.attr('index')].attr('source')
        if self.act_type == 'alxr':
            self.right_click_item_uri = self.tp_dct.get('rsv_re_uri', None) 
            self.right_click_item_name = None
            name_click = self.tp_dct.get('rsv_re_ename', None)
            try:
                if name_click:
                    self.right_click_item_name = (urllib.unquote(name_click.replace('\\x', '%'))
                                                    .decode('utf-8', 'ignore').encode('gb18030'))
            except:
                pass
        return 

    def asString(self):
        return self.__action.asString()

class MergeLogDispUrl:
    def __init__(self, url, se):
        self.url = se.attr('urls_list')[url.attr('url_index')].attr('url')
        self.pos = url.attr('url_index')
        self.url_type = url.attr('source')
        self.src_id = None
        if url.attr('source') == 'SP':
            self.src_id = url.attr('url_info.srcid')
        return 

class MergeLogSearch:
    def __init__(self, se):
        self.__se = se
        self.__disp_right = None
        self.actions = []
        self.disp_urls = []

        self.__is_ok = True
        if se.attr('urls_info') == [] or se.attr('actions_info') == []:
            # only have action or only have display info.
            print >> sys.stderr, 'reporter:counter:parse_err,url_action_not_both,1'
            self.__is_ok = False
            return 
        # append display urls.
        for url in se.attr('urls_info'):
            if url.attr('url_index') is not None:
                self.disp_urls.append( MergeLogDispUrl(url, se) )
        # query.
        query_info = se.attr('query_info')
        if not query_info:
            self.__is_ok = False
            print >> sys.stderr, 'reporter:counter:parse_err,no_query,1'
            return
        self.query = query_info.attr('original_query')
        if self.query is None:
            self.query = query_info.attr('query')
        if self.query is None:
            self.__is_ok = False
            print >> sys.stderr, 'reporter:counter:parse_err,no_query,1'
            return

        # F
        self.f = se.attr('query_info.f')
        # action
        tp = None
        for act in se.attr('actions_info'):
            self.actions.append( MergeLogAction(act, se) )
            if act.attr('fm') == 'se':
                tp = act.attr('tp')
        # rsv_dict.
        self.rsv_dict = {}
        if tp:
            fields = tp.split(":")
            for f in fields:
                if f.startswith("rsv_"):
                    try:
                        (k, v) = f.split("=")
                    except:
                        continue
                    self.rsv_dict[k] = v

    def disp_right(self):
        '''
            parse on use.
        '''
        if self.__disp_right is None:
            self.__disp_right = []
            for url in self.__se.attr('urls_info'):
                source = url.attr('source')
                if source == 'SPR':
                    right_card = MergeLogRightDisp()
                    if right_card.parse(url):
                        self.__disp_right.append( right_card )
        return self.__disp_right

    def is_ok(self): return self.__is_ok

class MergeLogGoals:
    def __init__(self, goal):
        self.searches = []
        for se in goal.attr('searches'):
            s = MergeLogSearch(se)
            if s.is_ok():
                self.searches.append( s )

class MergeLogMissions:
    def __init__(self, mi):
        self.goals = []
        for goal in mi.attr('goals'):
            self.goals.append(MergeLogGoals(goal))

class MergeLogSessions:
    def __init__(self, ml):
        self.missions = []
        for ms in ml.attr('missions'):
            self.missions.append(MergeLogMissions(ms))

class MergeLogParser:
    def __init__(self):
        self.__ml = log_parser.MergeLog_Protobuf()

    def iter_session(self):
        while True:
            try:
                flag = self.__ml.readNext()
            except Exception,e:#单行解析错误，或单行数据太大
                continue
            if flag < 0:#0文件结束，-1文件格式错误
                raise Exception('File format error!')
            if flag == 0:
                return 
            session = MergeLogSessions(self.__ml)
            yield session

    def iter_mission(self):
        for session in self.iter_session():
            for mission in session.missions:
                yield mission
    def iter_goal(self):
        for session in self.iter_session():
            for mission in session.missions:
                for goal in mission.goals:
                    yield goal
    def iter_search(self):
        while True:
            try:
                flag = self.__ml.readNext()
            except Exception,e:#单行解析错误，或单行数据太大
                continue
            if flag < 0:#0文件结束，-1文件格式错误
                break
            if flag == 0:
                return 
            for se in self.__ml.attr('searches'):
                search = MergeLogSearch(se)
                if search.is_ok():
                    yield search

if __name__=='__main__':
    psr = MergeLogParser()
    for goal in psr.iter_goal():
        for search in goal.searches:
            print 'search : %s, action: %d' % (search.query, len(search.actions))
