/***************************************************************************
 * 
 * Copyright (c) 2013 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/

/**
 * @file c_prod.cc
 * @author gusimiu(com@baidu.com)
 * @date 2013/06/26 14:15:34
 * @brief 
 *  
 **/
#include <python2.7/Python.h> //包含python的头文件

#include <map>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

#include "helper.h"

//#define __DEBUG__

struct output_matrix_t {
    float       **v;
    uint32_t    row;
    uint32_t    col;
    
    output_matrix_t():
        v(NULL),
        row(0),
        col(0)
    {}

    ~output_matrix_t() {
        release();
    }

    void release() {
        for (int i=0; i<row; ++i) {
            delete [] v[i];
        }
        delete [] v;
        v = NULL;
        row = 0;
        col = 0;
    }

    void alloc(uint32_t r, uint32_t c) {
        release();
        row = r;
        col = c;
        v = new float*[row];
        for (int i=0; i<col; ++i) {
            v[i] = new float[col];
            memset(v[i], 0, sizeof(float)*col);
        }
    }
};

struct pair_t {
    uint16_t index;
    float value;

    bool operator< (const pair_t& o) const {
        return index < o.index;
    }
};

struct vector_t {
    size_t num;
    pair_t pairs[512];

    vector_t(): num(0) {}

    void add(const pair_t& p) {
        pairs[num++] = p;
    }

    void sort() {
        ::sort(pairs, pairs+num);
    }
};

void matrix_dot(const vector<vector_t>& row_matrix, const map<int, vector_t>& col_matrix, output_matrix_t& out) {
    map<int, vector_t>::const_iterator it;
    for (int i=0; i<row_matrix.size(); ++i) {
        const vector_t* A = &row_matrix[i];
        for (int a=0; a<A->num; ++a) {
            uint16_t idx = A->pairs[a].index;
            float f = A->pairs[a].value;
            if ((it=col_matrix.find(idx)) == col_matrix.end()) {
                continue;
            }
            const vector_t& c_v = it->second;
            for (int b=0; b<c_v.num; ++b) {
                int vid = c_v.pairs[b].index;
                out.v[i][vid] += f * c_v.pairs[b].value;
            }
        }
    }
    return;
}

size_t pyl_size(PyObject* py_obj) {
    if (PyList_Check(py_obj)) {
        return PyList_Size(py_obj);
    } else {
        return PyTuple_Size(py_obj);
    }
}

PyObject* pyl_get_item(PyObject* py_obj, size_t i) {
    if (PyList_Check(py_obj)) {
        return PyList_GetItem(py_obj, i);
    } else {
        return PyTuple_GetItem(py_obj, i);
    }
}

void parse_matrix(
        PyObject* pvlist, 
        vector<vector_t>* row_matrix, 
        map<int, vector_t>* col_matrix) 
{
    size_t vsize = pyl_size(pvlist);
    for (size_t i=0; i<vsize; ++i) {
        // parse each vector.
        PyObject* v = pyl_get_item(pvlist, i);
        size_t s = pyl_size(v);    

        vector_t one_row;
        for (size_t j=0; j<s; ++j) {
            // parse each (index, value) pair.
            PyObject* ppair = pyl_get_item(v, j);

            pair_t inner_pair;
            inner_pair.index = PyInt_AsLong(pyl_get_item(ppair, 0));
            inner_pair.value = PyFloat_AsDouble(pyl_get_item(ppair, 1));
            if (row_matrix != NULL) {
                one_row.add(inner_pair);
            }

            if (col_matrix != NULL) {
                pair_t col_pair;
                col_pair.index = i; // index is row number.
                col_pair.value = inner_pair.value;
                (*col_matrix)[inner_pair.index].add(col_pair);
            }
        }
        if (row_matrix != NULL) {
            one_row.sort();
            (*row_matrix).push_back(one_row);
        }
    }
}

static PyObject * wrapper_self_dot(PyObject *self, PyObject *args) {
    Timer tm_parse, tm_proc, tm_pack;

    vector<vector_t> row_matrix;
    map<int, vector_t> col_matrix;

    tm_parse.begin();
    PyObject* pvlist = PyTuple_GetItem(args, 0);
    parse_matrix(pvlist, &row_matrix, &col_matrix);
    size_t row_count = row_matrix.size();
    tm_parse.end();

    tm_proc.begin();
    output_matrix_t out;
    out.alloc(row_count, row_count);
    matrix_dot(row_matrix, col_matrix, out);
    tm_proc.end();

    tm_pack.begin();
    PyObject* ret = PyTuple_New(row_count);
    for (size_t i=0; i<row_count; ++i) {
        PyObject* r = PyTuple_New(row_count);
        for (size_t j=0; j<row_count; ++j) {
            PyTuple_SetItem(r, j, PyFloat_FromDouble(out.v[i][j]));
        }
        PyTuple_SetItem(ret, i, r);
    }
    tm_pack.end();
    LOG_NOTICE("tm_all=%.4f tm_parse=%.4f tm_proc=%.4f tm_pack=%.4f", 
            tm_parse.cost_time()+tm_proc.cost_time()+tm_pack.cost_time(),
            tm_parse.cost_time(),
            tm_proc.cost_time(),
            tm_pack.cost_time());
    return Py_BuildValue("O", ret);
}

static PyObject * wrapper_dot(PyObject *self, PyObject *args) {
    vector<vector_t> row_matrix;
    map<int, vector_t> col_matrix;

    PyObject* A = PyTuple_GetItem(args, 0);
    PyObject* B = PyTuple_GetItem(args, 1);
    parse_matrix(A, &row_matrix, NULL);
    parse_matrix(B, NULL, &col_matrix);
    size_t row_count = row_matrix.size();
    size_t col_count = pyl_size(B);

    output_matrix_t out;
    out.alloc(row_count, col_count);
    matrix_dot(row_matrix, col_matrix, out);

    PyObject* ret = PyTuple_New(row_count);
    for (size_t i=0; i<row_count; ++i) {
        PyObject* r = PyTuple_New(col_count);
        for (size_t j=0; j<col_count; ++j) {
            PyTuple_SetItem(r, j, PyFloat_FromDouble(out.v[i][j]));
        }
        PyTuple_SetItem(ret, i, r);
    }
    return Py_BuildValue("O", ret);
}


// 3 方法列表
static PyMethodDef CProdFunc[] = {
    // Given two VectorList, return their dot output.
    { "dot", wrapper_dot, METH_VARARGS, 
        "Given two VectorList such as [[(index, vale), (index, value), ...], ...]. Return their dot output. out[i][j] indicates : dot(A[i], B[j])"},
    
    // Given a VectorList, return it's self-dot output.
    { "self_dot", wrapper_self_dot, METH_VARARGS, 
        "Given a VectorList such as [[(index, vale), (index, value), ...], ...]. Return it's self-dot output."},

    { NULL, NULL, 0, NULL }
};

// 4 模块初始化方法
PyMODINIT_FUNC initc_prod(void) {
    //初始模块，把CProdFunc初始到c_prod中
    PyObject *m = Py_InitModule("c_prod", CProdFunc);
    if (m == NULL)
        return;
}

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
