#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com

import argparse
import logging

from misc import *

class Arg(object):
	'''这个类就是非常简单封装argparse的类。
	使得更方便写而已
	iname : 简写
	'''
	def __init__(self, help='Lazy guy, no help'):
		self.is_parsed = False;
		help = s2s_ug(help)
		self.__parser = argparse.ArgumentParser(description=help)
		self.__args = None;
		# 辅助设置调试参数：
		#	-l --log 
		#		info : info级别调试
		#		debug : debug级别调试
		self.str_opt('log', 'l', '设置日志等级，和logging联动', 'error', meta='[debug|info|error]');
	def __default_tip(self, default_value=None):
		if default_value==None:
			return ''
		return ' default=[%s]'%default_value

	def bool_opt(self, name, iname, help=''):
		'''设置开关型配置
		'''
		help = s2s_ug(help)
		self.__parser.add_argument(
				'-'+iname, 
				'--'+name, 
				action='store_const', 
				const=1,
				default=0,
				help=help);
		return

	def str_opt(self, name, iname, help='', default=None, meta=None):
		'''设置字符串配置
		'''
		help = s2s_ug(help + self.__default_tip(default))
		self.__parser.add_argument(
				'-'+iname, 
				'--'+name, 
				metavar=meta,
				help=help,
				default=default);
		pass

	def var_opt(self, name, meta='', help='', default=None):
		'''不可丢变量
		'''
		help = s2s_ug(help + self.__default_tip(default))
		if meta=='':
			meta=name
		self.__parser.add_argument(name,
				metavar=meta,
				help=help,
				default=default) 
		pass

	def init_arg(self):
		if not self.is_parsed:
			self.__args = self.__parser.parse_args()
			self.is_parsed = True;
		if self.__args.log:
			format='%(asctime)s %(levelname)8s [%(filename)18s:%(lineno)04d]: %(message)s'
			if self.__args.log=='debug':
				logging.basicConfig(level=logging.DEBUG, format=format)
				logging.debug('log level set to [%s]'%(self.__args.log));
			elif self.__args.log=='info':
				logging.basicConfig(level=logging.INFO, format=format)
				logging.info('log level set to [%s]'%(self.__args.log));
			elif self.__args.log=='error':
				logging.basicConfig(level=logging.ERROR, format=format)
				logging.info('log level set to [%s]'%(self.__args.log));
			else:
				logging.error('log mode invalid! [%s]'%self.__args.log)
		return self.__args

	@property
	def args(self):
		if not self.is_parsed:
			self.__args = self.__parser.parse_args()
			self.is_parsed = True;
		return self.__args;


if __name__=='__main__':
	'''Test Code.
	'''
	a=Arg('中文帮助');
	a.var_opt('file');
	a.bool_opt('xml', 'x');
	a.str_opt('user', 'u', 'User Info.');
	a=a.init_arg();

	print a.user
	print a.file
	print a.xml
	

