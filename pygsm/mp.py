#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
#
# 	多进程相关库
# 	注意无法全局变量修改！
#

from multiprocessing import *
#import threading

import sys
import logging

class MPProcessor:
	'''多进程处理器
	给定进程数、处理函数和并发度，自动调度
	'''
	def __init__(self, functor, proc_num, stdout_dir='mp_out'):
		'''设定进程数和并发度
		'''
		self.functor = functor
		self.proc_num = proc_num
		self.processes = [];
		self.stdout_dir=stdout_dir;
		self.stdout_fn = [];
		for i in range(proc_num-1):
			self.processes.append(Process(target=self._inner_func, args=(i, )));
			out_fn = './%s/part-%05d'%(self.stdout_dir, i)
			self.stdout_fn.append(out_fn);
		# 补充一个thread num的FN
		out_fn = './%s/part-%05d'%(self.stdout_dir, self.proc_num)
		self.stdout_fn.append(out_fn);
		return

	def _inner_func(self, cur_i):
		'''
		多进程壳函数，调用真正的函数。同时做一些基本处理 
		'''
		# 先进行重定向
		old_stdout = sys.stdout;
		out_fn = self.stdout_fn[cur_i];
		logging.info('Process[%d] reset stdout to %s'%(cur_i, out_fn));
		sys.stdout = open( out_fn, 'w' )

		# 开始正式执行程序
		logging.info('Process[%d] begin to process.'%cur_i);
		# 执行进程函数、给定i和文件
		self.functor(cur_i, self.proc_num);

		sys.stdout = old_stdout; # 恢复bak stdout.
		logging.info('Process[%d] processes over.'%cur_i);

	def process_all(self):
		''' START => JOIN.
		'''
		for process in self.processes:
			process.start();
	
		# 自己也跑一个。
		self._inner_func(self.proc_num-1);

		for process in self.processes:
			process.join();


class MTItemProcessor(MPProcessor):
	'''对一个item集合的多线程处理方式
	给定set/list/dict等，和一个functor，即可分发到不同线程中调用
	TODO: 待测试
	'''
	def __init__(self, 
			proc_set, functor, proc_num, stdout_dir):
		MPProcessor.__init__(functor, proc_num, stdout_dir);
		self.proc_set = proc_set
		self.inner_func = functor
		self.functor = self._shell_functor
		return ;
	
	def _shell_functor(self, cur_i):
		'''真实的内嵌函数，进行集合遍历并输出
		'''
		for it in self.proc_set:
			if (id/7) % (self.proc_num+1) == cur_i:
				# hit this processor.
				self.inner_func(it);

	def merge_stdout(self):
		'''把所有文件统一输出
		'''
		logging.info('MTP: merge stdout');
		line_cnt = 0;
		for fn in self.stdout_fn:
			fl = open(fn, 'r');
			line = fl.readline();
			while line:
				line=line.rstrip('\n');
				print line;
				line_cnt += 1;
				line = fl.readline()
			fl.close();
		logging.info('MTP: merge over! %d lines written.'%line_cnt);

# test code.

def f(i):
	for u in range(100):
		print u*i

if __name__=='__main__':
	mpp = MPProcessor(functor=f, proc_num=10, stdout_dir='test_mpp_out');
	mpp.process_all();



