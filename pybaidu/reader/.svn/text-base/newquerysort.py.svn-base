#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

class QueryInfo:
    def __init__(self, query=None, freq=None, click=None, ratio_click=None):
        self.query = query
        self.freq = freq
        self.click = click
        self.ratio_click = ratio_click

class ClickInfo:
    def __init__(self, url=None, click=None, ratio_click=None, click_type=None):
        self.url = url
        self.click = click
        self.ratio_click = ratio_click
        self.click_type = click_type

    def is_normal_url(self):
        if self.url == '-':
            return False
        if self.url.find('http://')!=0:
            return False
        if self.url.find('http://ecom.fakeurl.baidu.com/')!=-1:
            return False
        return True

class DetailNewQuerySortProcessor:
    def __init__(self):
        pass

    def run(self, stream, handler):
        self.__handler = handler
        self.__process_init()
        while 1:
            line = stream.readline()
            if line == '':
                break
            arr = line.strip('\n').split('\t')
            query = arr[0]
            if query != self.__last_query:
                self.__end_query(query, arr)
            else:
                if len(arr)<10:
                    # some info is not well-formed.
                    # such as:
                    #   美金汇率 snippet_satisfy alop http://open.baidu.com/huilv/s?tn=baiduhuilv&wd=美金汇率 515
                    continue
                self.__click_info.append(
                        ClickInfo(
                            url = arr[9],
                            click = float(arr[7]),
                            click_type = arr[1],
                            ratio_click = float(arr[6]),
                                ) )
        self.__end_query(None, None)

    def __process_init(self):
        self.__last_query = None
        self.__last_query_info = None
        self.__click_info = []

    def __end_query(self, new_query, new_arr):
        if self.__last_query is not None:
            # call functor.
            self.__handler(self.__last_query_info, self.__click_info)

        self.__last_query = new_query
        self.__click_info = []
        self.__last_query_info = None
        if new_arr:
            if len(new_arr)<4:
                return
            self.__last_query_info = QueryInfo(
                    query = new_query,
                    freq = int(new_arr[1]), 
                    click = int(new_arr[3]), 
                    ratio_click = float(new_arr[2]))

if __name__=='__main__':
    pass
