#! /bin/env python
# encoding:utf-8

import sys
import cgi;

BootstrapCSSPath="http://cq01-2012h1-3-ranktest18.vm.baidu.com:8080/bootstrap/css/"
BootstrapJSPath="http://cq01-2012h1-3-ranktest18.vm.baidu.com:8080/bootstrap/js/"

def add_tag(doc, tag):
    '给文本添加标签输出'
    ret='<%s>\n%s\n</%s>' % (tag, doc, tag);
    return ret

#########################################
##   一些基本的元素
#########################################

class BObject:
    '''基本页面元素，主要有两个接口：
    __str__: 生成文档
    write: 在doc之后附加信息
    '''
    def __init__(self):
        self.doc = ''
        return 
    def __str__(self):
        return self.doc;
    def write(self, doc):
        inc = str(doc)
        self.doc += inc;
        return ;

class BKVPair(BObject):
    def __init__(self, key='', value=''):
        BObject.__init__(self)
        self.key = key;
        self.value = value;
    def __str__(self):
        return '<dt>%s</dt>\n<dd>%s</dd>\n' % (self.key, self.value)

class BLink(BObject):
    def __init__(self, link='', text='', target='_blank'):
        BObject.__init__(self)
        self.doc = '<a href="%s" target="%s">%s</a>' % (link, target, text)

class BKVList(BObject):
    '生成KVlist类型<dl></dl>'
    def __init__(self, horizontal=0):
        BObject.__init__(self)
        self.horizontal=horizontal
        self.kvpairs = []
    def clear(self):
        self.kvpairs = []
    def from_dict(self, dct):
        '从字典中生成数据，添加在原先的集合后面'
        for key in sorted(dct.keys()):
            kv = BKVPair(str(key), str(dct[key]))
            self.kvpairs.append(kv)
    def from_kvlist(self, kv_list):
        for key, value in kv_list:
            kv = BKVPair(str(key), str(value))
            self.kvpairs.append(kv)
    def __str__(self):
        hs=''
        if self.horizontal: hs=' class="dl-horizontal"'
        ret='<dl%s>\n' % hs;
        for it in self.kvpairs:
            ret += str(it)
        ret += '</dl>\n'
        return ret

class BSideBar(BObject):
    ''' 生成一个侧边栏，可以随着上下滚动而滚动
    每个链接跳转到#1位置
    '''
    def __init__(self, list, cut_length=-1, encoding='utf-8', span=4, offset=0): 
        self.__info_list = list
        self.__cut_length = cut_length
        self.__encoding = encoding
        self.__span = span
        self.__offset = offset
    def __str__(self):
        list_str=""
        for title, href in self.__info_list:
            if self.__cut_length>=0:
                title = title.decode(self.__encoding)
                if len(title)>=self.__cut_length:
                    title = title[0:self.__cut_length] + '...'
                title = title.encode(self.__encoding)
            list_str += '<li><a href="%s"><i class=\"icon-chevron-right\"></i> %s</a></li>' % (href, title);
        # 生成完整列表
        out_str = (
            '<div class="span%s offset%s bs-docs-sidebar">'
            '<ul class="nav nav-tabs nav-stacked affix", '
            'style="width:230px">'
            '%s'
            '</ul></div>') % (self.__span, self.__offset, list_str)
        return out_str

class BImg(BObject):
    '生成img结果'
    (Rounded, Circle, Polaroid)=range(3)
    def __init__(self, 
                img='', 
                cls=Rounded,
                width='',
                height=''):
        self.img = img
        self.cls = cls
        self.width=width
        if isinstance(width, int):
            self.width = '%dpx' % width
        self.height=height
        if isinstance(height, int):
            self.height = '%dpx' % height
        return
    def __str__(self):
        cls_code="img-rounded"
        if self.cls==BImg.Circle:
            cls_code="img_circle"
        elif self.cls==BImg.Polaroid:
            cls_code="img_polarioid"
        ws=''
        if self.width!='':
            ws='width:%s' % self.width
        hs=''
        if self.height!='':
            hs='height:%s' % self.height
        return '<img src="%s" class="%s" style="%s;%s">' % (self.img, cls_code, ws, hs)

class BDiv(BObject):
    'Div'
    def __init__(self, text='', cls='', offset=0):
        BObject.__init__(self)
        self.cls = cls
        self.offset = offset
        self.doc = text
    def __str__(self):
        offset_code = ''
        if self.offset>0:
            offset_code = ' offset%d' % self.offset
        return '<div class="%s%s">\n%s\n</div>\n' % (self.cls, offset_code, self.doc)

class BSpanDiv(BDiv):
    'Span div.'
    def __init__(self, text='', span=12, offset=0):
        span_code='span%d' % span
        BDiv.__init__(self, text, span_code, offset)
    def append(self, s):
        self.doc += str(s)

class BRowDiv(BDiv):
    'Row div.'
    def __init__(self, text='', offset=0):
        BDiv.__init__(self, text, 'row', offset)
    def append(self, s):
        self.doc += str(s)

class BPage(BObject):
    'page.'
    def __init__(self):
        BObject.__init__(self)
        return 
    def __str__(self):
        return add_tag(self.doc, 'html')

class BBody(BObject):
    '''生成body块
    '''
    def __init__(self):
        BObject.__init__(self)
        pass
    def __str__(self):
        return add_tag(self.doc, 'body')

class BHeader(BObject):
    '''生成Bootstrap头
    '''
    def __init__(self, 
                title='Support by Bootstrap.',
                css_path=BootstrapCSSPath,
                js_path=BootstrapJSPath):
        BObject.__init__(self)
        self.doc = '''
        <title>%s</title>

        <!-- Le styles -->
        <link href="%s/bootstrap.css" rel="stylesheet">
        <link href="%s/bootstrap-responsive.css" rel="stylesheet">
        <script type="text/javascript" charset="utf-8" src="%s/js/bootstrap.js"></script>
        ''' % (title, css_path, css_path, js_path)

    def __str__(self):
        return add_tag(self.doc, 'head');

class BNavigateBar(BObject):
    def __init__(self, title, item_list=None, sel_text=None, bottom='20px'):
        BObject.__init__(self)
        self.doc = ('<div class="navbar" style="margin-bottom:%s">'
            +'<div class="navbar-inner"><a class="brand" href="#">%s</a>') % (
                    bottom, title)
        self.doc += '<ul class="nav">'
        self.doc += '<li><a href="/">返回工具集</a></li>'
        if item_list:
            for url, text in item_list:
                if text == sel_text:
                    self.doc += '<li class="active"><a href="#">%s</a></li>' % sel_text
                else:
                    self.doc += '<li><a href="%s">%s</a></li>' % (url, text)
        self.doc += '</ul></div></div>'

class BButtonLink(BObject):
    def __init__(self, href, text, target="_blank", extra_class=''):
        self.doc = '<a class="btn %s" href="%s" target="%s">%s</a>' % (
                extra_class, href, target, text)

class BFooter(BObject):
    def __init__(self, text):
        self.doc = '<hr><div class="footer"><p>%s</p></div>' % text

class BSpanXRow(BObject):
    '''
        构造span=4,每行3个的多行
    '''
    def __init__(self, span=4, offset=0, count=3):
        BObject.__init__(self)
        self.__item_list = []
        self.__span = span
        self.__offset = offset
        self.__count = count

    def append(self, s):
        self.__item_list.append(str(s))

    def __str__(self):
        cnt = 0
        ret = ''
        row = BRowDiv(offset=self.__offset)
        for s in self.__item_list:
            row.append( BSpanDiv(s, span=self.__span) )
            cnt += 1
            if cnt==self.__count:
                ret += str(row)
                row = BRowDiv()
                cnt = 0
        if cnt!=0:
            ret += str(row)
        return ret

class BForm(BObject):
    def __init__(self, action=None, method='post'):
        BObject.__init__(self)
        self.action = action
        self.method = method
    def append(self, s):
        self.doc += str(s)
    def __str__(self):
        act = ''
        if self.action: 
            act = 'action="%s"' % self.action
        return '<form %s method="%s" class="form-horizontal">%s</form>' % (act, self.method, self.doc)

class BLegend(BObject):
    def __init__(self, s):
        BObject.__init__(self)
        self.doc = '<legend>%s</legend>' % s

class BLabel(BObject):
    def __init__(self, s):
        BObject.__init__(self)
        self.doc = '<label class="control-label">%s</label>' % (s)

class BTextInput(BObject):
    def __init__(self, name, value, place_holder=''):
        BObject.__init__(self)
        vs = ''
        if value:
            vs = 'value="%s"' % value
        self.doc = '<div class="controls"><input type="text" name="%s" %s placeholder="%s"></div>' % (
                name, vs, place_holder)

class BTextFieldInput(BObject):
    def __init__(self, name, value='', place_holder='', row=6, span=5):
        BObject.__init__(self)
        self.doc = '''<div class="controls">
                        <textarea rows="%d" class="span%d" name="%s" placeholder="%s">%s</textarea><br>
                    </div>''' % (
                row, span, name, place_holder, value)

class BLabelTextInput(BObject):
    def __init__(self, label, name, value, place_holder=''):
        BObject.__init__(self)
        l = BLabel(label)
        t = BTextInput(name, value, place_holder)
        self.doc = '<div class="control-group">' + str(l) + str(t) + '</div>'

class BButton(BObject):
    def __init__(self, label, extra_class=''):
        self.doc = ('<div class="control-group"><div class="controls">'
                        + '<button type="submit" class="btn %s">%s</button></div></div>'
                        % (extra_class, label) )

class BSelect(BObject):
    def __init__(self, label, name, li=[], selected=None):
        BObject.__init__(self)
        self.__label = label
        self.__name = name
        self.__list = li
        self.__selected = selected
    def append(self, s):
        self.__list.append(s)
    def __str__(self):
        ret = (str(BLabel(self.__label)) 
            + '<div class="control-group"><div class="controls"><select name="%s">' % (self.__name))
        for s in self.__list:
            if s == self.__selected:
                ret += '<option selected="selected">%s</option>' % s
            else:
                ret += '<option>%s</option>' % s
        ret += '</select></div></div>'
        return ret

class BError(BObject):
    def __init__(self, msg):
        BObject.__init__(self)
        self.doc = '<div class="alert alert-error">%s</div>' % msg

if __name__=='__main__':
    page = BPage();
    body = BBody();

    # gen a cont.
    cont = BSpanDiv(span=9, offset=0);

    # attach a image.
    img = BImg('http://hiphotos.baidu.com/zhixin/pic/item/5af4d7ea15ce36d3deca99023bf33a87e850b1f2.jpg',
            width='240')
    row = BRowDiv()
    row.write(BSpanDiv(span=3, doc=img))

    # attach a list.
    dct = { '生日':'1923-1-3', '身高':'184cm' }
    lst = BKVList(horizontal=1)
    lst.from_dict(dct)
    row.write(BSpanDiv(span=3, doc=lst))
    cont.write(row)

    row = BRowDiv(img)
    row.write(BSpanDiv(span=3, offset=0))
    row.write(cont)
    body.write(row)
    
    page.write(BHeader('This is a test title.'))
    page.write(body)

    print "Content-type: text/html; charset=utf-8\n"
    print page;
    pass





