# encoding=utf-8
# gusimiu@baidu.com

import ConfigParser
import os
import re
import logging

def get_processors_by_conf_str(str):
    ''' 给定一个配置字符串，读取各个包并且将他们new出来，
    读取如：
        conf=::type(param);path/A.py::b(param)
        那么返回一个list，包含逐个包含返回的对象 
    '''
    ret = []
    exec('from __main__ import *')
    for sth in str.split(';'):
        if sth=='':
            continue
        if sth.find('::')>=0:
            file, typename = sth.split('::')
        else:
            file=''
            typename=sth
        if file!='':
            # add path to os.path
            abspath = os.path.abspath(file)
            dir = os.path.dirname(abspath)
            bname = os.path.basename(abspath)
            pack = re.sub('\.py$', '', bname)
            logging.info('import package [%s] file [%s] at dir[%s]' % (pack, bname, dir))
            if dir not in sys.path:
                sys.path.append(dir)
            # import file.
            exec('from %s import *' % pack)
        # 创建一个新对象
        # 如果不带()，则给他加上一个
        if typename.find('(')==-1:
            typename = '%s()' % typename
        ret.append( eval('%s' % typename) )
        logging.info('Add processor: [[ %s ]]' % typename)
    return ret

def get_mapred_task_id():
    task_id = os.getenv('mapred_task_id')
    if task_id != None:
        s = re.search('(\d*)_\d*$', task_id)
        if s:
            return s.group(1)
    return None

def list_uniq(li):
    return {}.fromkeys(li).keys();

def whoami():
    import sys
    return sys._getframe(1).f_code.co_name

def conf_get(conf, sec, opt, default=None):
    if conf.has_option(sec, opt):
        return conf.get(sec, opt)
    return default

def load_var_dict_by_conf(conf, sec, dct=None):
    if dct==None:
        dct = {}
    for opt in conf.options(sec):
        dct[opt] = conf.get(sec, opt)
    return dct

def var_conf(conf, var_opt=None, var_sec=None):
    ''' 加强版conf：
        可以通过读取外部opt，或者var_sec字段获取变量
    '''
    var_dict = {}
    if var_sec:
        tmp_conf = ConfigParser.ConfigParser()
        tmp_conf.read(conf)
        for opt in tmp_conf.options(var_sec):
            var_dict[opt] = tmp_conf.get(var_sec, opt)
            logging.info('Load var: [%s]:[%s]' % (opt, var_dict[opt]))
    # load var opt, override the var in conf file.
    if var_opt:
        opts = var_opt.split(';')
        for kv in opts:
            k, v = kv.split('=')
            var_dict[k] = v
            logging.info('Load var: [%s]:[%s]' % (k, v))
    ret = ConfigParser.ConfigParser(var_dict)
    ret.read(conf)
    return ret

# 编码转换方式：
# u2s_u: unicode->str (utf-8)
# u2s_g: unicode->str (gb18030)
def u2s_u(uni):
    'unicode -> str (utf8)'
    return uni.encode( 'utf-8' );

def u2s_g(uni):
    'unicode -> str (gb18030)'
    return uni.encode( 'gb18030' );

def s2s_gu(s):
    'str(gb18030) -> str(utf8)'
    return s.decode('gb18030').encode('utf-8')

def s2s_ug(s):
    'str(utf8) -> str(gb18030)'
    return s.decode('utf-8').encode('gb18030')

def outstr(obj):
    '''将内建类型输出,
    如果是unicode，进行转码，否则直接输出
    '''
    if (type(obj)==type(unicode())):
        return u2s_g(obj);
    elif (type(obj)==type(list())):
        ret='[';
        for sth in obj:
            ret += str(sth) + ',';
        ret += ']';
        return ret;
    elif (type(obj)==type(dict())):
        ret='{';
        for ky in obj.keys():
            ret += "%s:%s, " % (str(ky), str(obj[ky]));
        ret += '}'
        return ret;
    else:
        return str(obj);

def str_kv(key, value):
    if value==None:
        return '';
    vs = outstr(value);
    return '%s = %s\n' % (u2s_g(key), vs);

def dct_get(dct, key, default=None):
    if dct.has_key(key):
        return dct[key];
    return default;

def dct_inc(dct, key, val=1):
    if not dct.has_key(key):
        dct[key] = val;
    else:
        dct[key] += val;

