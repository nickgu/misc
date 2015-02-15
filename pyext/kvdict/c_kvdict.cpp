/***************************************************************************
 * 
 * Copyright (c) 2013 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/

/**
 * @file test.cpp
 * @author gusimiu(com@baidu.com)
 * @date 2013/06/26 14:15:34
 * @brief 
 *      用Python的C接口实现一个词典类。
 *      可以弥补Python自带词典性能问题。
 *       内存KV词典：
 *       - 将文件读入Key-Value信息（目前局限都是文本）
 *       - 将哈希信息序列化到文件（方便在此调用）
 *       硬盘KV索引词典
 *       - 构建大文件的索引
 *  
 **/
#include <python2.7/Python.h> //包含python的头文件

#include <map>
#include <string>
#include <vector>
#include "ul_sign.h"
#include <ext/hash_map>
#include <ext/hash_set>

using namespace __gnu_cxx;
using namespace std;

/**
 *  文件位置表示：
 *      fid  : 对应文件ID
 *      bpos : 起始位置
 *      size : 块大小
 */
struct DiskData_t {
    size_t fid:4;
    size_t bpos:40;
    size_t size:20;
};

/* 内存KV词典：sign->data */
typedef hash_map<size_t, const char*> Dict_t;
typedef hash_map<size_t, DiskData_t> DiskDict_t;
typedef Dict_t::iterator DictIterator_t;

/**
 *  KVDict
 */
struct KVDict_t {
    // 当前词典是否是内存词典
    bool memory_mode;

    // 内存词典结构
    Dict_t dict;

    // 硬盘词典结构
    char buffer[1024*128];
    DiskDict_t disk_dict;
    vector<FILE*> fps;
};

/**
 *  内存数据信息
 */
struct KeyValue_t {
    size_t sign;
    DiskData_t value;
};

vector<KVDict_t*> g_dict_pool;

/**
 *  封装签名函数
 */
static size_t calc_sign(const char* s) {
    unsigned slen = strlen(s);
    unsigned low;
    unsigned high;
    creat_sign_f64((char*)s, slen, &low, &high);
    size_t ret = high;
    ret = (ret << 32LL) | low;
    return ret;
};

/**
 *  封装签名操作
 */
struct Sign_t {
    size_t operator() (const string& s) const {
        return calc_sign(s.c_str());
    }
};

/*
 * 随机访问文件获取一个数据
 */
int fgets_random(char* buffer,
                size_t buffer_size, 
                const vector<FILE*> fps, 
                const DiskData_t& d)
{
    if (d.fid<(size_t)0 || d.fid>=(size_t)fps.size()) {
        return -1;
    }
    FILE* fp = fps[d.fid];
    int ret = fseek(fp, d.bpos, SEEK_SET); 
    if (ret<0) {
        return ret;
    }
    buffer[d.size] = 0;
    return fread(buffer, d.size, 1, fp);
}

/**
 *  加载文件列表到词典
 */
int load(int dict_id, 
        int fcnt, 
        vector<char*> fn_list, 
        bool load_in_memory) 
{
    KVDict_t* pdict = g_dict_pool[dict_id];
    pdict->memory_mode = load_in_memory;
    //fprintf(stderr, "FCNT=%d LOADMEMORY=%d\n", fcnt, load_in_memory);
    char* line = pdict->buffer;
    size_t MAX_LINE_LENGTH = sizeof(pdict->buffer);
    int fid = 0;
    unsigned counter = 0;
    for (int id=0; id<fcnt; ++id) {
        FILE* fp = fopen(fn_list[id], "r");
        if (fp==NULL) {
            fprintf(stderr, "Cannot open file : %s\n", fn_list[id]);
            continue;
        }
        size_t fpos_b = ftell(fp);
        while (fgets(line, MAX_LINE_LENGTH, fp)) {
            unsigned line_len = strlen(line);
            // strip.
            line[line_len-1] = 0;
            size_t fpos_e = ftell(fp);

            size_t sign;
            const char* value_pos = "";
            unsigned value_length = 0;
            unsigned value_offset = 0;
            for (int i=0; line[i]; ++i) {
                if (line[i]=='\t') {
                    line[i] = 0;
                    value_pos = line+i+1;
                    value_offset = i+1;
                    value_length = line_len - i - 1;
                    break;
                }
            }
            sign = calc_sign(line);

            // 每一行都会被录入，如果只有一列，则整列作为key，value为空
            if (pdict->memory_mode) {
                char *content = new char[value_length + 1];
                strncpy(content, value_pos, value_length);
                content[value_length] = 0;
                pdict->dict[sign] = content;
            } else {
                DiskData_t d;
                d.fid = fid;
                d.bpos = fpos_b + value_offset;
                d.size = fpos_e - 1 - fpos_b - value_offset;
                pdict->disk_dict[sign] = d;
            }
            fpos_b = fpos_e;

            counter ++;
            if (counter % 1000000==0) {
                fprintf(stderr, "Load %d records over.\n", counter);
            }
        }
        if (pdict->memory_mode) {
            fclose(fp);
        } else {
            pdict->fps.push_back(fp);
            fid ++;
        }
    }
    fprintf(stderr, "LoadDictOver! Dsize=%u DiskIndexSize=%u\n", 
            pdict->dict.size(), 
            pdict->disk_dict.size());
    return 0;
}

int has(int dict_id, const char* k) 
{
    KVDict_t* pdict = g_dict_pool[dict_id];
    string key = k;
    size_t sign = calc_sign(key.c_str());
    if (pdict->memory_mode) {
        if (pdict->dict.find(sign)==pdict->dict.end()) {
            return 0;
        }
    } else {
        if (pdict->disk_dict.find(sign)==pdict->disk_dict.end()) {
            return 0;
        }
    }
    return 1;
}

int seek(int dict_id, 
        const char* k, 
        string& out) 
{
    KVDict_t* pdict = g_dict_pool[dict_id];
    string key = k;
    size_t sign = calc_sign(key.c_str());
    if (pdict->memory_mode) {
        if (pdict->dict.find(sign)==pdict->dict.end()) {
            return 0;
        }
        out = pdict->dict[sign];
    } else {
        if (pdict->disk_dict.find(sign)==pdict->disk_dict.end()) {
            return 0;
        }
        DiskData_t d = pdict->disk_dict[sign];
        fgets_random(pdict->buffer, sizeof(pdict->buffer), pdict->fps, d);
        out = string(pdict->buffer);
    }
    return 1;
}

static PyObject * wrapper_create(PyObject *self, PyObject *args)  {
    int did = g_dict_pool.size();
    // create new.
    g_dict_pool.push_back(new KVDict_t());
    return Py_BuildValue("i", did);
}

// 2 python 包装
static PyObject * wrapper_load(PyObject *self, PyObject *args) 
{
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    int fcnt = PyInt_AsLong(PyTuple_GetItem(args, 1));
    vector<char*> fn_list; 
    PyObject *flist = PyTuple_GetItem(args, 2);
    for (int i=0; i<fcnt; ++i) {
        PyObject* o = PyList_GetItem(flist, i);
        char* fn = PyString_AsString(o);
        fn_list.push_back(fn);
    }
    bool load_in_memory = (bool)PyInt_AsLong(PyTuple_GetItem(args, 3));

    int ret = load(did, fcnt, fn_list, load_in_memory);
    return Py_BuildValue("i", ret);//把c的返回值n转换成python的对象
}

/**
 * 将内存词典写到文件
 */
static PyObject * wrapper_write_mem_bin(PyObject *self, PyObject *args) {
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    char* output_filename = PyString_AsString(PyTuple_GetItem(args, 1));

    fprintf(stderr, "Writting: %d, out_fn: %s\n", did, output_filename);
    if (did<0 || did>=(int)g_dict_pool.size()) {
        return Py_BuildValue("i", -1);
    }
    FILE* fp = fopen(output_filename, "w");
    if (fp==NULL) {
        return Py_BuildValue("i", -1);
    }

    KVDict_t* dict = g_dict_pool[did];
    u_int num = dict->dict.size();
    fwrite(&num, sizeof(num), 1, fp);
    fprintf(stderr, "writing : %u\n", num);
    for (Dict_t::iterator it=dict->dict.begin();
            it!=dict->dict.end(); it++)
    {
        fwrite(&it->first, sizeof(it->first), 1, fp);
        size_t len = strlen(it->second)+1;
        fwrite(&len, sizeof(size_t), 1, fp);
        fwrite(it->second, len, 1, fp);
    }

    fclose(fp);
    return Py_BuildValue("i", 0);//把c的返回值n转换成python的对象
}

static PyObject * wrapper_load_mem_bin(PyObject *self, PyObject *args)
{
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    char* input_name = PyString_AsString(PyTuple_GetItem(args, 1));
    if (did<0 || did>=(int)g_dict_pool.size()) {
        return Py_BuildValue("i", -1);
    }
    KVDict_t* dict = g_dict_pool[did];
    dict->memory_mode = true;
    dict->dict.clear();
    dict->dict.resize(10000000);

    FILE* fp = fopen(input_name, "r");
    if (fp == NULL) {
        fprintf(stderr, "Cannot open file [%s] to read.\n", input_name);
        return Py_BuildValue("i", -1); 
    }
    size_t curpos = ftell(fp);
    fseek(fp, 0L, SEEK_END);
    size_t fsize = ftell(fp);
    fseek(fp, curpos, SEEK_SET);
    char *big_buffer = new char[fsize];
    fread(big_buffer, sizeof(char), fsize, fp);

    char * cur = big_buffer;
    u_int num = (*(u_int*)cur);
    cur += sizeof(u_int);
    fprintf(stderr, "Load bin. (%u to loads) [filesize=%u]\n", num, fsize);
    for (u_int i=0; i<num; ++i) {
        size_t sign, len;
        sign = (*(size_t*)cur);
        cur += sizeof(size_t);
        len = (*(size_t*)cur);
        cur += sizeof(size_t);

        dict->dict[sign] = cur;
        //printf("%u :L=%u: %s\n", sign, len, cur);
        cur += len;
    }

    fclose(fp);
    return Py_BuildValue("i", 0);//把c的返回值n转换成python的对象
}

/**
 *  将硬盘词典的索引写到文件中
 */
static PyObject * wrapper_write_index(PyObject *self, PyObject *args)
{
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    char* output_filename = PyString_AsString(PyTuple_GetItem(args, 1));

    fprintf(stderr, "Writting: %d, out_fn: %s\n", did, output_filename);
    if (did<0 || did>=(int)g_dict_pool.size()) {
        return Py_BuildValue("i", -1);
    }
    FILE* fp = fopen(output_filename, "w");
    if (fp==NULL) {
        return Py_BuildValue("i", -1);
    }
    KVDict_t* dict = g_dict_pool[did];
    unsigned block_num = dict->disk_dict.size();
    KeyValue_t *data = new KeyValue_t[block_num];
    unsigned i=0;
    fwrite(&block_num, sizeof(block_num), 1, fp);
    for (DiskDict_t::iterator it=dict->disk_dict.begin();
            it!=dict->disk_dict.end(); it++)
    {
        data[i].sign = it->first;
        data[i++].value = it->second;
    }
    fwrite(data, sizeof(KeyValue_t), block_num, fp);
    fclose(fp);
    delete [] data;
    return Py_BuildValue("i", 0);//把c的返回值n转换成python的对象
}

static PyObject * wrapper_load_index_and_file(PyObject *self, PyObject *args)
{
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    char* index_file_name = PyString_AsString(PyTuple_GetItem(args, 1));
    int flist_cnt = PyInt_AsLong(PyTuple_GetItem(args, 2)); 
    PyObject* flist = PyTuple_GetItem(args, 3); 

    if (did<0 || did>=(int)g_dict_pool.size()) {
        return Py_BuildValue("i", -1);
    }
    KVDict_t* dict = g_dict_pool[did];
    dict->memory_mode = false;
    dict->fps.clear();
    dict->disk_dict.clear();

    fprintf(stderr, "dict_id: %d, index_file_name: %s file_count: %d\n", did, index_file_name, flist_cnt);
    for (int i=0; i<flist_cnt; ++i) {
        PyObject* o = PyList_GetItem(flist, i);
        char* fn = PyString_AsString(o);
        fprintf(stderr, "ADD_FILE: %s\n", fn);
        dict->fps.push_back( fopen(fn, "r") );
    }
    FILE* index_fp = fopen(index_file_name, "r");
    unsigned block_count;
    fread(&block_count, sizeof(unsigned), 1, index_fp);
    fprintf(stderr, "Load index. (%d to loads)\n", block_count);
    KeyValue_t * data = new KeyValue_t[block_count];
    fread(data, sizeof(KeyValue_t), block_count, index_fp);
    for (unsigned i=0; i<block_count; ++i) {
        dict->disk_dict[data[i].sign] = data[i].value;
    }
    delete [] data;
    return Py_BuildValue("i", 0);//把c的返回值n转换成python的对象
}

static PyObject * wrapper_seek(PyObject *self, PyObject *args) {
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    const char* key = PyString_AsString(PyTuple_GetItem(args, 1));
    if (key == NULL) {
        fprintf(stderr, "KVDict: parse input key failed! key is NULL.");
        Py_INCREF(Py_None);
        return Py_None;
    }
    string out;
    int found = seek(did, key, out);
    if (found) {
        return Py_BuildValue("s", out.c_str());
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

static PyObject * wrapper_has(PyObject *self, PyObject *args) {
    int did = PyInt_AsLong(PyTuple_GetItem(args, 0));
    const char* key = PyString_AsString(PyTuple_GetItem(args, 1));
    int found = has(did, key);
    return Py_BuildValue("i", found);
}

// 3 方法列表
static PyMethodDef CKVDictFunc[] = {
    // 创建一个词典
    { "create", wrapper_create, METH_VARARGS, "create a dict."},
    // 读取文件到词典，可选是否是内存结构
    { "load", wrapper_load, METH_VARARGS, "load files into dict."},
    // 查找信息
    { "find", wrapper_seek, METH_VARARGS, "search dict. return None if not exists."},
    // 是否包含特定key
    { "has", wrapper_has, METH_VARARGS, "check key in dict."},
    // 将内存词典序列化到文件
    { "write_mem_bin", wrapper_write_mem_bin, METH_VARARGS, "write mem-dict to bin file." },
    // 读取序列化好的文件
    { "load_mem_bin", wrapper_load_mem_bin, METH_VARARGS, "load mem-dict to bin file." },
    // 将索引写到硬盘
    { "write_index",  wrapper_write_index, METH_VARARGS, "write dict to index-file."},
    // 将索引和对应的文件读入到硬盘词典
    { "load_index_and_files", wrapper_load_index_and_file, METH_VARARGS, "load index and files to memory." },
    { NULL, NULL, 0, NULL }
};
// 4 模块初始化方法
PyMODINIT_FUNC initc_kvdict(void) {
    //初始模块，把CKVDictFunc初始到c_kvdict中
    PyObject *m = Py_InitModule("c_kvdict", CKVDictFunc);
    if (m == NULL)
        return;
}

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
