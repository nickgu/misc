#! /bin/env python
# encoding=utf-8
#
#   V1.1:
#       change pygsm.misc and pygsm.arg to pydev.
#       make it possible to support multi-configuration loaded.
#       such as:
#           [common_job]
#           .. some config ..
#
#           [derived_job]
#           .. more config ..
#
#   V1.0.1:
#       add mapinstream.
#   V1.0:
#       complete.
#

import logging
import sys
import os

class HadoopProcessor(object):
    (
        LineFunctor, 
        FieldFunctor
    ) = range(2)
    def __init__(self, my_type=FieldFunctor):
        print >> sys.stderr, '[%s] managed.' % (self.__class__.__name__)
        self.__type = my_type

    def type(self): return self.__type
    def process_line(self, line): pass
    def process_fields(self, fields): pass
    def end_process(self): pass

class HadoopApp(object):
    def __init__(self):
        self.__processor = {}

    def set_processor(self, proc, key='-'):
        self.__processor[key] = proc

    def run(self, key='-'):
        proc = self.__processor[key]()
        P = lambda p, l: p.process_line(l)
        if proc.type() == HadoopProcessor.FieldFunctor:
            P = lambda p, l: p.process_fields(l.strip('\n').split('\t'))

        while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            P(proc, line)
        proc.end_process()

class HadoopBin(object):
    '''hadoop程序
    '''
    def __init__(self, hadoop=''):
        '设置程序'
        self.__hadoop = hadoop

    def run(self,
            job_name,
            input,
            output,
            mapper,
            reducer,
            file = [],
            mapper_num=-1,
            mapper_capacity=-1,
            reducer_num=-1,
            reducer_capacity=-1,
            priority="HIGH",
            extra_jobconf=[],
            cmdenv=[],
            archive=[],
            partitioner=None,
            cmd='streaming',
            queue=None,
            groups=None,
            mapinstream=None,
            inputformat=None,
            outputformat=None):
        logging.info('JOB [[ %s ]]' % job_name)
        logging.info('INPUT: %s' % input)
        logging.info('OUTPUT: %s' % output)

        cmd = '%s %s' % (self.__hadoop, cmd)
        cmd += '  -jobconf mapred.job.name="%s"' % job_name

        # 可选选项
        if groups:
            cmd += '  -jobconf mapred.job.groups=%s' % groups
        if queue:
            cmd += '  -jobconf mapred.job.queue.name="%s"' % queue
        if mapper_num:
            cmd += '  -jobconf mapred.map.tasks=%d' % mapper_num
        if mapper_capacity:
            cmd += '  -jobconf mapred.job.map.capacity=%d' % mapper_capacity
        if reducer_num:
            cmd += '  -jobconf mapred.reduce.tasks=%d' % reducer_num
        if reducer_capacity:
            cmd += '  -jobconf mapred.job.reduce.capacity=%d' % reducer_capacity
        if mapinstream:
            cmd += '  -mapinstream %s' % mapinstream
        if inputformat:
            cmd += '  -inputformat %s' % inputformat
        if outputformat:
            cmd += '  -outputformat %s' % outputformat

        # add cmdenv
        for kv in cmdenv:
            if len(kv)<=0:
                continue
            cmd += '  -cmdenv %s' % (kv)
        # add jobconf.
        for jobconf in extra_jobconf:
            if len(jobconf)<=0:
                continue
            cmd += '  -jobconf %s' % jobconf
        # add archive
        for arc in archive:
            if len(arc)<=0:
                continue
            cmd += '  -cacheArchive "%s"' % arc
        if partitioner!=None:
            cmd += '  -partitioner %s' % partitioner

        # 输入
        if not input:
            raise Exception('Hadoop: streaming input missed!')
        # input是一个数组或者字符串
        if isinstance(input, list):
            for item in input:
                cmd += '  -input "%s"' % item
        elif isinstance(input, str):
            cmd += '  -input "%s"' % input

        # 输出
        if not output:
            raise Exception('Hadoop: streaming output missed!')
        cmd += '  -output %s' % output
        if not mapper:
            logging.warning('Hadoop: mapper is None.')
            mapper= 'None'
        cmd += '  -mapper %s' % mapper
        if not reducer:
            logging.warning('Hadoop: reducer is None.')
            reducer= 'None'
        cmd += '  -reducer %s' % reducer
        if file:
            for f in file:
                if len(f)<=0:
                    continue
                cmd += '  -file "%s"' % f
        # 增加对python库的支持
        cmd += '  -cmdenv "PYTHONPATH=."'

        if priority:
            cmd += '  -jobconf mapred.job.priority="%s"' % (priority)
        logging.info(cmd.replace('  ', '\n\t'))
        # 执行
        print cmd
        return os.system(cmd)
            
    def fs(self, fscmd):
        cmd = '%s fs -%s' % (self.__hadoop, fscmd)
        logging.info(cmd)
        return os.system(cmd)

    def fsget(self, hdfs_path, local_path):
        cmd = '%s fs -get %s %s' % (self.__hadoop, hdfs_path, local_path)
        logging.info(cmd)
        return os.system(cmd)

    def rmdir(self, dr):
        ret=os.system('%s fs -test -d %s' % (self.__hadoop, dr))
        if ret==0:
            ret=os.system('%s fs -rmr %s' % (self.__hadoop, dr))

def proc_streaming_job(hadoop, conf, sec):

    # get info from conf.
    input = conf.get(sec, 'input').split(',')
    output = conf.get(sec, 'output')
    mapper = conf.get(sec, 'mapper', default='NONE')
    reducer = conf.get(sec, 'reducer', default='NONE')
    cmd = conf.get(sec, 'command', default='streaming')
    mapper_num = conf.get(sec, 'mapper_num', default=None)
    if mapper_num!=None:
        mapper_num = int(mapper_num)
    reducer_num = conf.get(sec, 'reducer_num', default=None)
    if reducer_num!=None:
        reducer_num = int(reducer_num)
    mapper_capacity = conf.get(sec, 'mapper_capacity', default=None)
    if mapper_capacity!=None:
        mapper_capacity = int(mapper_capacity)
    reducer_capacity = conf.get(sec, 'reducer_capacity', default=None)
    if reducer_capacity!=None:
        reducer_capacity = int(reducer_capacity)


    files = conf.get(sec, 'files', default='').split(',')
    priority = conf.get(sec, 'priority', default='HIGH')
    partitioner = conf.get(sec, 'partitioner', default=None)
    extra_jobconf = conf.get(sec, 'extra_jobconf', default='').split(',')
    cmdenv = conf.get(sec, 'cmdenv', default='').split(',')
    archive = conf.get(sec, 'archive', default='').split(',')
    queue = conf.get(sec, 'queue', default=None)
    groups = conf.get(sec, 'groups', default=None)
    mapinstream = conf.get(sec, 'mapinstream', default=None)
    inputformat = conf.get(sec, 'inputformat', default=None)
    outputformat = conf.get(sec, 'outputformat', default=None)

    # rmr old output.
    hadoop.rmdir(output)
    # run streamming.
    return hadoop.run(job_name=sec,
                input=input,
                output=output,
                file=files,
                mapper=mapper,
                reducer=reducer,
                mapper_num=mapper_num,
                mapper_capacity=mapper_capacity,
                reducer_num=reducer_num,
                reducer_capacity=reducer_capacity,
                priority=priority,
                extra_jobconf=extra_jobconf,
                cmdenv=cmdenv,
                archive=archive,
                partitioner=partitioner,
                cmd=cmd,
                queue=queue,
                groups=groups,
                mapinstream=mapinstream,
                inputformat=inputformat,
                outputformat=outputformat)

def proc_fs_job(hadoop, conf, sec):
    cmd_num = int(conf.get(sec, 'cmd_num'))
    for i in range(cmd_num):
        cmd_no = i+1
        cmd = conf.get(sec, 'cmd%d'%cmd_no)
        ret=hadoop.fs(cmd)
        if ret!=0:
            logging.error('Execute cmd=[%s] failed.' % cmd)
            return -1
    return 0

def process_hadoop_job(hadoop, conf, job):
    logging.info('Process job [%s]' % job)
    # 如果是复合型job，则先运行子任务
    if conf.has_option(job, 'combine'):
        jobs = conf.get(job, 'jobs').split(',')
        for sub_job in jobs:
            if sub_job=='':
                continue
            ret=process_hadoop_job(hadoop, conf, sub_job)
            if ret!=0:
                return ret
    else:
        type = conf.get(job, 'type', default='streaming')
        if type=='fs':
            return proc_fs_job(hadoop, conf, job)
        else:
            ret= proc_streaming_job(hadoop, conf, job)
            return ret
    return 0

if __name__=='__main__':
    import pydev
    from pygsm.arg import *

    arg = Arg('Hadoop封装程序')
    arg.str_opt('var', 'v', '引入变量，用于配置 sample="a=b;c=d"')
    arg.str_opt('conf', 'c', '任务配置文件', default='hadoop.conf')
    arg.str_opt('job', 'j', '任务名称，可以是逗号分隔的序列任务, 如果没有，则执行raw_input命令。', default=None)
    arg.str_opt('exe', 'e', '单行fs任务，如果不存在job，则优先执行-e命令，否则从stdin读取fs命令')
    opt = arg.init_arg()

    logging.info('Try to load var_conf at opt=[%s]' % opt.var)
    conf = pydev.VarConfig()
    conf.read(opt.conf.split(','), 
            pydev.dict_from_str(opt.var, l1_sep=';', l2_sep='='), 
            var_sec='var')

    # load global info.
    sec = 'hadoop'
    hadoop_bin = conf.get(sec, 'hadoop')
    hadoop = HadoopBin(hadoop_bin)

    if opt.job==None:
        if opt.exe!=None:
            hadoop.fs(opt.exe)
        else:
            logging.info('No job input, so change to interative command mode.')
            while 1:
                cmd = raw_input()
                hadoop.fs(cmd)
    else:
        for job in opt.job.split(','):
            print >> sys.stderr, 'Process job[%s]' % job
            if not conf.has_section(job):
                print >> sys.stderr, 'No job named [%s]' % job
            for key, value in conf.items(job):
                logging.info('%s.%s=%s' % (job, key, value))
            ret=process_hadoop_job(hadoop, conf, job)
            if ret!=0:
                sys.exit(-1)
    logging.info('HADOOP.PY : PROCESS OK.')
    sys.exit(0)


