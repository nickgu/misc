#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import os
import sys
import time
import ConfigParser
import re
import copy

from zxdb.arg import *
from zxdb.tool import *

def load_context_from_conf(config, section, raw=False):
    ''' 提供默认的从配置
        操作机制：从config的section域读取信息。
        由于config可能已经带上var信息，所以不直接使用配置名。
    '''
    context = {}
    for opt in config.options(section):
        context[opt] = config.get(section, opt, raw)
    return context

class JobBase(object):
    'Job Interface.'
    #def _on_init(self, **context): pass
    def _proc(self, **context): pass

    def __init__(self, jobname=None, copy_from=None):
        self.__init_context = {}
        self._name = jobname
        self.__begin_time = 0
        self.__end_time = 0
        self.__diff_time = 0

        if copy_from!=None:
            for k, v in copy_from.context.iteritems():
                self.__init_context[k] = v

    def set_name(self, name):
        self._name = name

    # 设置不覆盖环境变量
    def set_extra_context(self, **context):
        for k, v in context.iteritems():
            if k not in self.__init_context:
                self.__init_context[k] = v

    def set_context(self, **context):
        for k, v in context.iteritems():
            self.__init_context[k] = v

    @property
    def context(self): return self.__init_context;

    def set_jobfactory(self, jobfactory):
        self._jobfactory = jobfactory

    def run(self, **context): 
        self.__startup(**context)
        # 用运行时变量系统和以前存储的变量汇聚，然后执行
        dct = self.__context_dict(context)
        self._proc(**dct)
        self.__end()
        # run本身不处理错误。但会抛出异常

    def get_job(self, jobname):
        return self._jobfactory.get_job(jobname)
    
    def __startup(self, **context):
        logging.info('Job:[%s] start.' % self._job_name())
        self.__begin_time = time.time()

    def __end(self):
        self.__end_time = time.time()
        self.__diff_time = self.__end_time - self.__begin_time
        logging.info('Job:[%s] end. Use time [[ %d second(s) ]]' % (
            self._job_name(), self.__diff_time))

    def _job_name(self): 
        return self._name
        #return '%s:%s' % (type(self), str(self._name))

    def __context_dict(self, cur_context_dict):
        ''' 三部分变量系统：
            按从上到下合并数据
            self._jobfactory.get_var_dict() : 全局变量
            self.__init_context : 基础变量
            cur_context_dict
        '''
        ret={}
        for k, v in self._jobfactory.get_var_dict().iteritems():
            ret[k] = v
        for k, v in self.__init_context.iteritems():
            ret[k] = v
        for k, v in cur_context_dict.iteritems():
            ret[k] = v
        # interpolate all.
        for k, v in ret.iteritems():
            if not isinstance(v, str):
                continue
            ret[k] = self.__interpolate(v, ret)
        return ret

    def __interpolate(self, rawval, vars):
        ''' code from ConfigParser()
        '''
        # do the string interpolation
        value = rawval
        depth = self.MAX_INTERPOLATION_DEPTH
        while depth:                    # Loop through this until it's done
            depth -= 1
            if value and "%(" in value:
                value = self._KEYCRE.sub(self._interpolation_replace, value)
                try:
                    value = value % vars
                except KeyError, e:
                    raise Exception(('InterpolationMissingOptionError v=[%s]\n'
                            '\tbad value=%s\n'
                            '\tvals=%s\n') 
                            % (value, e, vars))
            else:
                break
        if value and "%(" in value:
            raise Exception('InterpolationDepthErro')
        return value

    MAX_INTERPOLATION_DEPTH = 32
    _KEYCRE = re.compile(r"%\(([^)]*)\)s|.")
    def _interpolation_replace(self, match):
        s = match.group(1)
        if s is None:
            return match.group()
        else:
            return "%%(%s)s" % s.lower()

class JobManager(object):
    def __init__(self):
        self.__job_dict = {}
        self.__var_dict = {} # 全局变量词典

        # 待加载的package
        self.__pack_list = []
        # 待加载的conf
        self.__conf_list = []

    def load(self, confs=[]):
        # 先从各个文件中读取[.job]域
        self.__conf_list = filter(lambda x:x!='', confs)
        for conf in self.__conf_list:
            self.__load_preinclude_info(conf)
        logging.info('After pre-include, CONF_LIST=%s' % self.__conf_list)
        for conf in self.__conf_list:
            self.__load_var_conf(conf)
        for conf in self.__conf_list:
            self.__load_job_conf(conf)

    def set_global_var(self, name, value):
        self.__var_dict[name] = value

    def __load_preinclude_info(self, conf):
        sec = '.job'
        config=ConfigParser.ConfigParser()
        config.read(conf)
        if not config.has_section(sec):
            return 
        # 导入python文件和包
        if config.has_option(sec, 'files'):
            files=config.get(sec, 'files').split(',')
            for f in files:
                self.__import_file(f)
        # 导入更多job 配置
        if config.has_option(sec, 'job_files'):
            files=config.get(sec, 'job_files').split(',')
            files.reverse()
            for x in files:
                if x not in self.__conf_list:
                    self.__conf_list.insert(0, x)
        # 导入var_conf
        if config.has_option(sec, 'var_files'):
            files=config.get(sec, 'var_files').split(',')
            files.reverse()
            for x in files:
                if x not in self.__conf_list:
                    self.__conf_list.insert(0, x)

    def __load_var_conf(self, var_conf):
        sec = '.var'
        config = ConfigParser.ConfigParser(self.__var_dict)
        config.read(var_conf)
        if not config.has_section(sec):
            return 
        logging.info('Load Var File: %s' % var_conf)
        tmp_dct = load_context_from_conf(config, sec)
        for k, v in tmp_dct.iteritems():
            self.__var_dict[k] = v

    def __load_job_conf(self, job_conf):
        # 默认都从job读取需要读取的任务信息
        logging.info('Load Job File : %s' % job_conf)
        # 导入任务
        config=ConfigParser.ConfigParser()
        config.read(job_conf)
        for job in config.sections():
            if job=='':
                continue
            if job[0] == '.':
                continue

            if config.has_option(job, '__job_template'):
                # 从模板生成任务
                ts = config.get(job, '__job_template')
                jobtemp = self.__get_job_template(ts)
                jobinstance = jobtemp()
                logging.debug('Init Job [[%s]] from template : [[%s]]' % (job, ts))
            elif config.has_option(job, '__job_type'):
                # 从任务生成任务
                jobtype = config.get(job, '__job_type')
                from_job = self.get_job(jobtype)
                jobinstance = type(from_job)(copy_from=from_job)
                logging.debug('Init Job [[%s]] from other job [[%s]]'% (job, jobtype))
            else:
                logging.info('JobDefinitionError [[%s]]: no __job_template and no __job_type' % job)
                continue

            # 读取任务值定义的是时候，不做值替换。
            context = load_context_from_conf(config, job, raw=True)
            jobinstance.set_context(**context)
            self.register_job(job, jobinstance)

    def register_job(self, name, job_instance):
        if name in self.__job_dict:
            logging.error('Job [[ %s ]] has already been in factory.' % name)
        self.__job_dict[name] = job_instance
        job_instance.set_name(name)
        logging.info( 'Load job : [[%s]]' % (name) )

    def get_job(self, name):
        if name not in self.__job_dict:
            logging.error(self.__job_dict.keys())
            raise Exception('JOB [[ %s ]] NOT FOUND.' % name)
        self.__job_dict[name].set_jobfactory(self)
        return self.__job_dict[name]

    def get_var_dict(self):
        return self.__var_dict

    def __get_job_template(self, s):
        for pack in self.__pack_list:
            exec('from %s import *' % pack)
        return eval(s)

    def __import_file(self, file):
        abspath = os.path.abspath(file)
        dir = os.path.dirname(abspath)
        bname = os.path.basename(abspath)
        pack = re.sub('\.py$', '', bname)
        # add path.
        if dir not in sys.path:
            sys.path.append(dir)
        # add packname for import.
        self.__pack_list.append(pack)
        logging.info('import [%s] file [%s] at dir[%s]' % (pack, bname, dir))

if __name__=='__main__':
    arg=Arg()
    arg.str_opt('jobs', 'j', '需要执行的任务')
    arg.str_opt('conf', 'c', '配置文件', default='')
    opt=arg.init_arg()

    # load from conf.
    jf = JobManager()
    jf.load(opt.conf.split(','))
    mail_job = jf.get_job('JobType_Alert')
    for job in opt.jobs.split(','):
        try:
            j = jf.get_job(job)
            j.run()
        except Exception, msg:
            logging.error(msg)
            mail_job.run(title='ZhixinBuildFailed', job_name=job)




