# encoding=utf-8
import cgi;
import urlparse

class Page:
    def __init__(self):
        self.fheader=''; # 文件头
        self.head=''; # html header
        self.body=''; # html body.
        self.set_header();

        # get param_set.
        self._form = cgi.FieldStorage();
        return ;

    def set_header(self, doctype='text/html', charset='utf-8'):
        '''设置Header
        '''
        self.fheader="Content-type: " + doctype + "; charset=" + charset + '\n\n';

    def prhead(self, s):
        self.head += str(s) + '\n';

    def prbody(self, s):
        self.body += str(s) + '\n';

    def get_param(self, opt, default_value=None):
        '''获取参数
        '''
        uname=default_value;
        if opt in self._form:
            uname = self._form[opt].value;
        return uname;

    def draw_page(self):
        print (
'''%s
<html>
<head>%s</head>
<body>
%s
</body>
</html>
''' % (self.fheader, self.head, self.body));


class BootstrapPage(Page):
    def __init__(self, title='Supported by Bootstrap!', environ=None):
        Page.__init__(self)
        self.set_header()
        self.__environ = environ
        self.__get_param_dict = None
        if self.__environ:
            qs = environ['QUERY_STRING']
            if qs:
                self.__get_param_dict = urlparse.parse_qs(qs)
        
        self.head = '''
        <title>%s</title>
        <!-- IE Compatible -->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

        <!-- Le styles -->
        <link href="/bootstrap/css/bootstrap.css" rel="stylesheet">
        <link href="/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
        <script src="/jquery.js"></script>
        <script type="text/javascript" charset="utf-8" src="/bootstrap/js/bootstrap.js"></script>
        ''' % (title)

    def add_js(self, js):
        self.head += '<script src="%s"></script>\n' % js

    def add_css(self, css):
        self.head += '<link href="%s" rel="stylesheet">\n' % css

    def draw_page(self):
        print (
'''%s<!doctype html>
<html>
<head>%s</head>
<body>
%s
</body>
</html>
''' % (self.fheader, self.head, self.body));

    def str_page(self):
        ret= (
'''<!doctype html>
<html>
<head>%s</head>
<body>
<div class="container">
<div class="row">
%s
</div>
</div>
</body>
</html>
''' % (self.head, self.body));

        return ret;

