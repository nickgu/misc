#!/usr/bin/env python
#coding=utf-8

"""
author: huanghaiyuan(@baidu.com)
date: 2013/08/17
version: 1.1
description:
    Structs that used to hold user click infos.
    You can test this program by:
        cat newcookiesort | python newcookiesort_parser.py debug 1>output 2>err
    or ignore the 'debug' option:
        cat newcookiesort | python newcookiesort_parser.py 1>output 2>err


"""

import sys

global debug
debug = False

def DEBUG_INFO(debug_info):
    """
    description: you can use this global function wherever you wanna print some log.
            But pls infer that, only work when you run the program with 'debug' option.
    """
    if debug:
        print >> sys.stderr,"[DEBUG] %s"%debug_info

SPLIT1 = "\t"
SPLIT2 = ":"
SPLIT3 = "="

IdxDict1 = {"COOKIE":0,
        "IP":1,
        "TIME":2,
        "FM":3,
        "PN":4,
        "P1":5,
        "P2":6,
        "P3":7,
        "P4":8,
        "TN":9,
        "TAB":10,
        "TITLE":11,
        "TP":12,
        "f":13,
        "RSP":14,
        "F":15,
        "QUERY":16,
        "URL":17,
        "BDUSS":18,
        "WEIGHT":19, # USELESS
        "ID":20,
        "INFO":21,
        "PREFIX_SUG":22,
        "MU":23,
        "S":24,
        "OQ":25,
        "QID":26,
        "CID":27
        }

IdxDict2 = {"GIDX":0,
        "SATISFACTION":1,
        "CLICK_WEIGHT":2,
        "NS_F":3,
        "USER_DELAY":4,
        "F1":5,
        "F2":6,
        "F3":7,
        "INPUT_T":8,
        "UID":9}

class QueryInfo(object):
    def __init__(self, action_eles):
        self.query = action_eles[IdxDict1["QUERY"]]
        self.oq = action_eles[IdxDict1["OQ"]]
        self.prefix_sug = action_eles[IdxDict1["PREFIX_SUG"]]
        self.f = action_eles[IdxDict1["f"]]
        if action_eles[IdxDict1["RSP"]].isdigit():
            self.rsp = int(action_eles[IdxDict1["RSP"]])
        else:
            self.rsp = -1
        infos = getInfos(action_eles)
        self.ns_f = infos[IdxDict2["NS_F"]]
        if infos[IdxDict2["INPUT_T"]].isdigit():
            self.inputT = int(infos[IdxDict2["INPUT_T"]])
        else:
            self.inputT = -1

    def toString(self):
        return "\t".join(map(str, (self.query,
            self.oq,
            self.prefix_sug,
            self.f,
            self.rsp)))

def getInfos(action_eles):
    """
    description: return the splited infos
    """
    info = action_eles[IdxDict1["INFO"]]
    info_list = info.split( SPLIT2 )
    return info_list

def make_rsv(tp):
    """
    description: split rsvs into a dict
    """
    rsv_dict = {}
    if tp == None:
        return rsv_dict

    rsvs = tp.split( SPLIT2 )
    for rsv in rsvs:
        kv = rsv.split( SPLIT3 )
        if len(kv) != 2:
            continue
        key, value = kv[0], kv[1]
        rsv_dict[key] = value
    return rsv_dict


class Action(object):
    def __init__(self, action_eles):
        self.datetime = action_eles[IdxDict1["TIME"]]
        self.fm = action_eles[IdxDict1["FM"]]
        self.click_pos = int(action_eles[IdxDict1["P1"]])
        self.rsv_dict = None
        self.page_no = -2

        # set sub click
        p2 = action_eles[IdxDict1["P2"]]
        p3 = action_eles[IdxDict1["P3"]]
        p4 = action_eles[IdxDict1["P4"]]
        p2 = -1 if p2 == "-" else int(p2)
        p3 = -1 if p3 == "-" else int(p3)
        p4 = -1 if p4 == "-" else int(p4)
        if p2 > 0:
            self.click_subtype = 1
            self.click_subpos = p2
        elif p3 > 0:
            self.click_subtype = 2
            self.click_subpos = p3
        elif p4 > 0:
            self.click_subtype = 3
            self.click_subpos = p4
        else:
            self.click_subtype = 0
            self.click_subpos = -1

        self.click_url = action_eles[IdxDict1["URL"]]
        self.click_mu = action_eles[IdxDict1["MU"]]
        self.click_title = action_eles[IdxDict1["TITLE"]]
        self.tab = action_eles[IdxDict1["TAB"]]
        self.tp = action_eles[IdxDict1["TP"]]
        self.rsv_dict = make_rsv(self.tp)
        info_list = getInfos(action_eles)
        self.is_satisfied = True if info_list[IdxDict2["SATISFACTION"]] == "1" else False
        self.new_weight = float(info_list[IdxDict2["CLICK_WEIGHT"]])
        self.page_no = int(action_eles[IdxDict1["PN"]])


    def finish(self, **argv):
        pass

    def get_rsv(self, rsv_name, default_value=None):
        name = rsv_name
        if not rsv_name.startswith("rsv_"):
            name = "rsv_" + rsv_name

        if name not in self.rsv_dict:
            return default_value
        else:
            return self.rsv_dict[name]

    def printSelf(self):
        sys.stdout.write("\t") # for indentation
        print "\t".join(map(str,(
            self.datetime,
            self.fm,
            self.click_pos,
            self.click_url,
            self.click_mu,
            self.click_title,
            self.tab,
            self.tp,
            self.is_satisfied,
            self.new_weight)))

class Search(object):
    def __init__(self):
        self.ip = None
        self.datetime = None
        self.qid = []
        self.page_no = None
        self.tn = None
        self.sample_id = None # cid
        self.user_delay = -1
        self.tp = None
        self.tab = None
        self.rsv_dict = None
        self.satisfaction = False # queryrank
        self.action_type = None # queryrank

        self.actions = [] # list of Action
        self.query_info = None # QueryInfo

    def finish(self, **argv):
        for action in self.actions:
            action.finish()

    def get_rsv(self, rsv_name, default_value=None):
        name = rsv_name
        if not rsv_name.startswith("rsv_"):
            name = "rsv_" + rsv_name

        if name not in self.rsv_dict:
            return default_value
        else:
            return self.rsv_dict[name]

    def printSelf(self):
        DEBUG_INFO("action count=%d"%len(self.actions))
        sys.stdout.write("\t") # for indentation
        print "\t".join(map(str, (
            self.query_info.toString(),
            self.ip,
            self.datetime,
            self.qid[0],
            self.page_no,
            self.tn,
            self.sample_id,
            self.tp
            )))
        for idx, action in enumerate(self.actions):
            action.printSelf()

    def _mk_basics(self, action_eles):

        self.ip = action_eles[IdxDict1["IP"]]
        self.datetime = action_eles[IdxDict1["TIME"]]
        self.qid.append(action_eles[IdxDict1["QID"]])
        self.page_no = int(action_eles[IdxDict1["PN"]])
        self.tn = action_eles[IdxDict1["TN"]]
        self.sample_id = action_eles[IdxDict1["CID"]]

        infos = getInfos(action_eles)
        self.user_delay = float(infos[IdxDict2["USER_DELAY"]])

        self.tab = action_eles[IdxDict1["TAB"]]

        self.tp = action_eles[IdxDict1["TP"]]
        self.rsv_dict = make_rsv(self.tp)

        queryrank = action_eles[IdxDict1["S"]].split(":")
        if len(queryrank) == 2:
            self.satisfaction = True if queryrank[0]=="1" else False
            self.action_type = queryrank[1]

        self.query_info = QueryInfo(action_eles)

    def is_new(self, action_eles):
        fm = action_eles[IdxDict1["FM"]]
        query = action_eles[IdxDict1["QUERY"]]
        if fm in ("se",):
            page_no = action_eles[IdxDict1["PN"]]
            # a new search action
            if page_no == "-1":
                return True
            elif self.query_info and query != self.query_info.query:
                return True
            # query are the same and page_no is not "-1", indicates a turn page action
            else:
                self.qid.append(action_eles[IdxDict1["QID"]])
                return False
        # clicks
        else:
            # in newcookiesort, turn page action could be missed.
            # so, qid is not a proper way to judge the same search
            # and we take that, all the clicks follow a search, should
            # be in the search, no matter what its qid is.
            """
            qid = action_eles[IdxDict1["QID"]]
            if qid == self.qid[-1]:
                return False
            else:
                return True
            """
            return False


    def addAction(self, action_eles):
        fm = action_eles[IdxDict1["FM"]]
        query = action_eles[IdxDict1["QUERY"]]
        if fm in ("se",):
            page_no = action_eles[IdxDict1["PN"]]
            # search action
            if page_no == "-1":
                self._mk_basics(action_eles)
                DEBUG_INFO("added a search")
            # turn page
            elif self.query_info and query == self.query_info.query:
                self.actions.append(Action(action_eles))
            # invalid
            else:
                raise TypeError("Nether search nor turn page action:\n%s"%str(action_eles))
        # clicks
        else:
            DEBUG_INFO("added a click")
            self.actions.append(Action(action_eles))

class Goal(object):
    def __init__(self):
        self.searches = [] # indice of searches
        self.gid = "-1" # goal index

    def finish(self, **argv):
        for search in self.searches:
            search.finish()

    def is_new(self, action_eles):
        """
        description: judge the action is in current goal, only depends on goal-index
        return: True if action can be added in this Goal instance; False, otherwise
        """
        info_list =  getInfos(action_eles)
        gid = info_list[IdxDict2["GIDX"]]
        if self.gid == gid:
            return False
        else:
            return True

    def addAction(self, action_eles):
        # decide which search this action belongs to
        if not self.searches or self.searches[-1].is_new(action_eles):
            self.searches.append(Search())
            info_list = getInfos(action_eles)
            self.gid = info_list[IdxDict2["GIDX"]]
        search = self.searches[-1]

        search.addAction(action_eles)

    def printSelf(self):
        for idx, search in enumerate(self.searches):
            search.printSelf()
        sys.stdout.write("\n") # to seperate different goals

class Session(object):
    def __init__(self):
        self.goals = [] # indice of goals

    def finish(self, **argv):
        for goal in self.goals:
            goal.finish()

    def empty(self):
        if self.goals:
            return False
        else:
            return True

    def is_new(self, action_eles):
        """
        description: judge the action_eles is in current session
        return: True if action_eles can be added in this Session instance; False, otherwise
        """
        # read in an empty line
        if not action_eles:
            # if current session is new, then new coming action should be in this session
            if not self.goals:
                return False
            # if current session is not new, then new coming action is another session
            else:
                return True
        # if not empty, then action should be in current session
        else:
            return False

    def addAction(self, action_eles):
        # decide which goal this action belongs to
        if not self.goals or self.goals[-1].is_new(action_eles):
            self.goals.append(Goal())
        goal = self.goals[-1]

        goal.addAction(action_eles)

    def printSelf(self):
        for idx, goal in enumerate(self.goals):
            print "\tgoal %d"%idx
            goal.printSelf()


class CookieInfo(object):
    def __init__(self, action_eles):
        self.cookie = action_eles[IdxDict1["COOKIE"]]
        self.is_registered = True if action_eles[IdxDict1["BDUSS"]] == "1" else False
        info_list = getInfos(action_eles)
        self.uid = -1
        if info_list[IdxDict2["UID"]]:
            try:
                self.uid = int(info_list[IdxDict2["UID"]])
            except ValueError:
                pass
        #self.uid = -1 if info_list[IdxDict2["UID"]] else int(info_list[IdxDict2["UID"]])

        self.sessions = [] # list of Session
        # not used currently
        #self.searches = [] # list of Search

    def finish(self, **argv):
        """
        description:
            Bebore use current instance, user should call this method to calculate some statistics.
        """

        # because of our session split algorithm, the last session could be empty
        # for user's sake, we remove empty session
        if self.sessions[-1].empty():
            self.sessions.remove(self.sessions[-1])

        for session in self.sessions:
            session.finish()

    def is_new(self, action_eles):
        if not action_eles:
            return False

        cookie = action_eles[IdxDict1["COOKIE"]]
        if cookie == self.cookie:
            return False
        else:
            return True

    def addAction(self, action_eles):

        # decide which session the action_eles belong
        if not self.sessions or self.sessions[-1].is_new(action_eles):
            DEBUG_INFO("New Session")
            self.sessions.append(Session())
        session = self.sessions[-1]

        if action_eles:
            session.addAction(action_eles)

        # if cookie has at least one register action, then we take the cookie as a registered user
        if action_eles and action_eles[IdxDict1["BDUSS"]] == "1" and not self.is_registered:
            self.is_registered = True

            info_list = getInfos(action_eles)
            if info_list[IdxDict2["UID"]]:
                try:
                    self.uid = int(info_list[IdxDict2["UID"]])
                except ValueError:
                    pass

    def printSelf(self):
        DEBUG_INFO("call cookie.printSelf")
        # cookie infos
        print "\t".join(map(str, (self.cookie, self.is_registered, self.uid)))

        # session infos
        for idx, session in enumerate(self.sessions):
            print "session %d"%idx
            session.printSelf()
        print "\n" # to seperate different cookies

################# test here #####################

def cookie_flow(stream):
    cookie_info = None
    for line in stream:
        line = line.strip()

        action_list = []
        if line:
            action_list = line.split(SPLIT1)

        DEBUG_INFO("read in: %s"%line)

        if not action_list and not cookie_info:
            DEBUG_INFO("Empty line and Empty cookie_info")
            continue

        if not cookie_info or cookie_info.is_new(action_list):
            DEBUG_INFO("New cookie info")
            if cookie_info:
                cookie_info.finish() # before you use the cookie_info instance, you should invoke finish method to make sure some statistics are calculated
                #cookie_info.printSelf() # in your own app, you should treat with your own logic instead print it out
                yield cookie_info
                DEBUG_INFO("printed a cookie info")
            if not action_list:
                continue
            cookie_info = CookieInfo(action_list)

        cookie_info.addAction(action_list)
        DEBUG_INFO("added an action")

    if cookie_info:
        cookie_info.finish() # before you use the cookie_info instance, you should invoke finish method to make sure some statistics are calculated
        #cookie_info.printSelf() # in your own app, you should treat with your own logic instead print it out
        yield cookie_info
        DEBUG_INFO("End of file")

class NewCookiesortParser:
    def __init__(self):
        pass
    def iter_cookie(self, stream):
        for cookie in cookie_flow(stream):
            yield cookie
    def iter_session(self, stream):
        for cookie in cookie_flow(stream):
            for session in cookie.sessions:
                yield session
    def iter_goal(self, stream):
        for cookie in cookie_flow(stream):
            for session in cookie.sessions:
                for goal in session.goals:
                    yield goal
    def iter_search(self, stream):
        for cookie in cookie_flow(stream):
            for session in cookie.sessions:
                for goal in session.goals:
                    for search in goal.searches:
                        yield search

if "__main__" == __name__:

    debug_tag = ""
    #global debug
    debug = False
    if len(sys.argv) != 1:
        debug_tag = sys.argv[1]

    if debug_tag == "debug":
        debug = True

    # in your own app, you should wrap codes like below
    for cookie_info in cookie_flow(sys.stdin):
        cookie_info.printSelf()

