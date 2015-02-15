#! /bin/env python
# encoding=utf-8

# gusimiu@baidu.com
# 对大文件进行分割处理和读取统一调用函数处理

import random
import argparse

from linestream import *

class FileSpliter:
	def __init__(self, 
			out_num = 10,
			out_dir = 'split_out'):
		'''
		以及划分输出目录，part数量
		并依此打开文件
		'''
		self.part_num = out_num;
		self.out_dir = out_dir;
		self.fl = [];
		for i in range(0, self.part_num):
			fn = '%s/part-%05d' % (self.out_dir, i);
			fl = open(fn, 'w');
			self.fl.append(fl);

	def write(self, sth):
		pno = random.randint(0, self.part_num-1);
		self.fl[pno].write(sth);

	def close(self):
		for fl in self.fl:
			fl.close();

if __name__=='__main__':
	'''
	测试代码，几种应用：
		1. 多行文件拆分
		2. 
	'''
	parser = argparse.ArgumentParser(description='Split big file by line.')
	parser.add_argument('file', metavar='FILE') 
	parser.add_argument('-x', '--item_xml', action='store_const', const=1,
			help='Whether use <item> to split xml file.');
	
	args = parser.parse_args()
	spl = FileSpliter(10)
	if args.item_xml:
		ls = LineStream(args.file);
		ls.postline_handler = SubLineHandler(r'</item>', LineStream.ItemEnd);
		ls.preline_handler = SubLineHandler(r'<item>', LineStream.ClearBuffer);
		for item in ls.streaming():
			spl.write(item);
	else:
		ls = LineFile(args.file)
		for line in ls.iter_line():
			spl.write(line);
	spl.close();
