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

#define __OUTPUT_TIMESTAT_INFO__
#define __USE_HASH_MAP__
#define __HASH_SIZE__ (128)

#ifdef __USE_HASH_MAP__
    #include <ext/hash_map>
#else
    #include <map>
#endif

#include <string>
#include <vector>
#include <algorithm>
using namespace std;

#include "helper.h"

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
        if (row>0 && col>0) {
            //LOG_NOTICE("out: free");
            for (uint32_t i=0; i<row; ++i) {
                delete [] v[i];
            }
            delete [] v;
        }
        v = NULL;
        row = 0;
        col = 0;
    }

    void alloc(uint32_t r, uint32_t c) {
        release();
        row = r;
        col = c;
        if (r>0 && c>0) {
            //LOG_NOTICE("out: new");
            v = new float*[row];
            for (uint32_t i=0; i<col; ++i) {
                v[i] = new float[col];
                memset(v[i], 0, sizeof(float)*col);
            }
        }
    }
};

struct pair_t {
    uint32_t    index;
    float       value;

    bool operator< (const pair_t& o) const {
        return index < o.index;
    }
};

struct vector_t {
    const static size_t BufferSize = 256;

    size_t num;
    size_t size;
    pair_t *pairs;

    vector_t(): 
        num(0),
        size(0),
        pairs(NULL)
    {}

    vector_t(const vector_t& o) {
        num = o.num;
        size = o.size;
        if (size > 0) {
            //LOG_NOTICE("vector: malloc");
            pairs = (pair_t*)malloc(sizeof(pair_t) * size);
            memcpy(pairs, o.pairs, sizeof(pair_t)*num);
        } else {
            pairs = NULL;
        }
    }

    ~vector_t() {
        size = 0;
        num = 0;
        if (pairs) {
            //LOG_NOTICE("vector: free");
            free(pairs);
        }
    }

    void add(const pair_t& p) {
        if (num + 1>size) {
            size += BufferSize;
            if (pairs == NULL) {
                //LOG_NOTICE("vector: malloc");
                pairs = (pair_t*)malloc( sizeof(pair_t)*size );
            } else {
                pairs = (pair_t*)realloc(pairs, sizeof(pair_t)*size );   
            }
        }
        pairs[num++] = p;
    }

    void sort() {
        ::sort(pairs, pairs+num);
    }
};

class column_matrix_t {
#ifdef __USE_HASH_MAP__
    typedef __gnu_cxx::hash_map<int, vector_t*> ColumnDict_t;
#else
    typedef map<int, vector_t*> ColumnDict_t;
#endif

    public:
#ifdef __USE_HASH_MAP__
        column_matrix_t():
            _col_index(__HASH_SIZE__) {}
#endif

        void add_column_info(uint32_t col, pair_t col_info) {
            if (_col_index.find(col) == _col_index.end()) {
                //LOG_NOTICE("map:new");
                _col_index[col] = new vector_t();
            }
            _col_index[col]->add(col_info);
        }

        const vector_t* get_column(uint32_t col) const {
            if (_col_index.find(col) == _col_index.end()) {
                return NULL;
            } 
            return _col_index.find(col)->second;
        }

        ~column_matrix_t() {
            for (ColumnDict_t::iterator it = _col_index.begin();
                    it!=_col_index.end(); ++it) 
            {
                if (it->second != NULL) {
                    //LOG_NOTICE("map:delete");
                    delete it->second;
                }    
            }
        }

    private:
        ColumnDict_t _col_index;
};

void matrix_dot(const vector<vector_t>& row_matrix, const column_matrix_t& col_matrix, output_matrix_t& out) {
    for (size_t i=0; i<row_matrix.size(); ++i) {
        const vector_t* A = &row_matrix[i];
        for (uint32_t a=0; a<A->num; ++a) {
            uint32_t idx = A->pairs[a].index;
            float   f = A->pairs[a].value;

            const vector_t* p_col = col_matrix.get_column(idx);
            if (p_col == NULL) {
                continue;
            }
            for (uint32_t b=0; b<p_col->num; ++b) {
                int vid = p_col->pairs[b].index;
                out.v[i][vid] += f * p_col->pairs[b].value;
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
        column_matrix_t* col_matrix) 
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
                col_matrix->add_column_info(inner_pair.index, col_pair);
            }
        }
        if (row_matrix != NULL) {
            one_row.sort();
            (*row_matrix).push_back(one_row);
        }
    }
}

static PyObject * wrapper_self_dot(PyObject *self, PyObject *args) {
#ifdef __OUTPUT_TIMESTAT_INFO__
    Timer tm;
    tm.begin();
#endif

    vector<vector_t> row_matrix;
    column_matrix_t col_matrix;

    PyObject* pvlist = PyTuple_GetItem(args, 0);
    parse_matrix(pvlist, &row_matrix, &col_matrix);
    size_t row_count = row_matrix.size();

    output_matrix_t out;
    out.alloc(row_count, row_count);
    matrix_dot(row_matrix, col_matrix, out);

    PyObject* ret = PyList_New(row_count);
    for (size_t i=0; i<row_count; ++i) {
        PyObject* r = PyList_New(row_count);
        for (size_t j=0; j<row_count; ++j) {
            PyObject* v = PyFloat_FromDouble(out.v[i][j]);
            PyList_SetItem(r, j, v);
            //Py_XDECREF(v);
        }
        PyList_SetItem(ret, i, r);
        //Py_XDECREF(r);
    }

#ifdef __OUTPUT_TIMESTAT_INFO__
    tm.end();
    LOG_NOTICE("SELF_DOT tm_all=%.4f", tm.cost_time());
#endif
    return ret;
}

static PyObject * wrapper_dot(PyObject *self, PyObject *args) {
#ifdef __OUTPUT_TIMESTAT_INFO__
    Timer tm;
    tm.begin();
#endif
    vector<vector_t> row_matrix;
    column_matrix_t col_matrix;

    PyObject* A = PyTuple_GetItem(args, 0);
    PyObject* B = PyTuple_GetItem(args, 1);
    parse_matrix(A, &row_matrix, NULL);
    parse_matrix(B, NULL, &col_matrix);
    size_t row_count = row_matrix.size();
    size_t col_count = pyl_size(B);

    output_matrix_t out;
    out.alloc(row_count, col_count);
    matrix_dot(row_matrix, col_matrix, out);

    PyObject* ret = PyList_New(row_count);
    for (size_t i=0; i<row_count; ++i) {
        PyObject* r = PyList_New(col_count);
        for (size_t j=0; j<col_count; ++j) {
            PyList_SetItem(r, j, PyFloat_FromDouble(out.v[i][j]));
        }
        PyList_SetItem(ret, i, r);
    }
#ifdef __OUTPUT_TIMESTAT_INFO__
    tm.end();
    LOG_NOTICE("DOT tm_all=%.4f", tm.cost_time());
#endif
    return ret;
}

void parse_vector(PyObject* v, vector_t* out) {
    size_t s = pyl_size(v);    
    for (size_t j=0; j<s; ++j) {
        // parse each (index, value) pair.
        PyObject* ppair = pyl_get_item(v, j);

        pair_t inner_pair;
        inner_pair.index = PyInt_AsLong(pyl_get_item(ppair, 0));
        inner_pair.value = PyFloat_AsDouble(pyl_get_item(ppair, 1));
        out->add(inner_pair);
    }
    out->sort();
}

static PyObject * wrapper_dot_1d(PyObject *self, PyObject *args) {
    // try faster calculation.
#ifdef __OUTPUT_TIMESTAT_INFO__
    Timer tm;
    tm.begin();
#endif
    PyObject* obj_A = PyTuple_GetItem(args, 0);
    PyObject* obj_B = PyTuple_GetItem(args, 1);
    vector_t A, B;
    parse_vector(obj_A, &A);
    parse_vector(obj_B, &B);

    float ret = 0.0;
    uint32_t b=0;
    for (uint32_t a=0; a<A.num; ++a) {
        uint32_t idx = A.pairs[a].index;
        float   f = A.pairs[a].value;

        while (b<B.num) {
            uint32_t ib = B.pairs[b].index;
            if (ib >= idx) {
                if (ib == idx) {
                    ret += f * B.pairs[b].value;
                }
                break;
            }
            b ++;
        }
    }
#ifdef __OUTPUT_TIMESTAT_INFO__
    tm.end();
    LOG_NOTICE("DOT_1D tm_all=%.4f", tm.cost_time());
#endif
    return Py_BuildValue("f", ret);
}

// 3 方法列表
static PyMethodDef CProdFunc[] = {
    // Given two VectorList, return their dot output.
    { "dot", wrapper_dot, METH_VARARGS, 
        "Given two VectorList such as [[(index, vale), (index, value), ...], ...]. Return their dot output. out[i][j] indicates : dot(A[i], B[j])"},

    // Given two Vector, return their dot output.
    { "dot_1d", wrapper_dot_1d, METH_VARARGS, 
        "Given two Vector such as [(i, v)..]. Return their dot output."},
    
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
