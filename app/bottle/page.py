# encoding=utf-8
import cgi;

class Page:
	def __init__(self):
		self.fheader=''; # 文件头
		self.head=''; # html header
		self.body=''; # html body.
		self.set_header();

		# get param_set.
		self.form = cgi.FieldStorage();
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
		if opt in self.form:
			uname = self.form[opt].value;
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
	def __init__(self, title='Supported by Bootstrap!'):
		Page.__init__(self)
		self.set_header()
		
		self.head = '''
    	<title>%s</title>

	    <!-- Le styles -->
    	<link href="/bootstrap/css/bootstrap.css" rel="stylesheet">
    	<link href="/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
		''' % (title)

	def draw_page(self):
		print (
'''%s<!doctype html>
<html>
<head>%s</head>
<body>
<div class="container">
%s
</div>
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

