/***************************************************************************
 * 
 * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file pagerank.cpp
 * @author gusimiu(com@baidu.com)
 * @date 2014/04/18 09:20:14
 * @brief 
 *  
 **/

#include <cmath>

#include <string>
#include <vector>
#include <map>
#include <stdexcept>

class MemPagerank {
    public:
        MemPagerank(float damp=0.85f):
            _damp(damp), 
            _target(NULL),
            _pagerank(NULL),
            _node_num(0)
        {}

        /* trainning process.*/
        void add_node(const std::string& node_label);
        void begin_iteration();
        /**
         * return the accumulated diff in this iteration.
         */
        float stop_one_iteration();
        void process_edge(const std::string& label_A, 
                        const std::string& label_B, 
                        float prob);

        /* access function. */
        float pagerank(const std::string& node_label) const;

        void dump_all(FILE* fp) const;

    private:
        size_t label_to_id(const std::string& node_label) const;

        std::map<std::string, size_t>   _label_id_dict;
        size_t  _pagerank_size;
        float   _damp;

        size_t  _node_num;

        float*  _pagerank;
        float*  _target;
        float*  _pagerank_buffer[2];
};

float 
MemPagerank::pagerank(const std::string& node_label) const
{
    size_t node_id = label_to_id(node_label);
    if (_pagerank==NULL || _pagerank_size<=node_id) {
        throw std::logic_error("Pagerank buffer is not good.");
    }
    return _pagerank[node_id];
}

size_t 
MemPagerank::label_to_id(const std::string& s) const {
    std::map<std::string, size_t>::const_iterator it = _label_id_dict.find(s);
    if (it == _label_id_dict.end()) {
        throw std::logic_error(std::string("label_to_id failed to find key [") 
                + s + std::string("]."));
    }
    return it->second;
}

void 
MemPagerank::add_node(const std::string& node_label) 
{
    if (_label_id_dict.find(node_label) != _label_id_dict.end()) {
        return;
    }
    size_t cur_id = _label_id_dict.size();
    _label_id_dict[node_label] = cur_id;
}

void 
MemPagerank::begin_iteration() 
{
    _node_num = _label_id_dict.size();
    _pagerank_buffer[0] = new float[_node_num];
    _pagerank_buffer[1] = new float[_node_num];
    _pagerank = _pagerank_buffer[0];
    _target   = _pagerank_buffer[1];
    for (size_t i=0; i<_node_num; ++i) {
        _pagerank[i] = 10.0f;
        _target[i] = (1.0f - _damp) / (_node_num);
    }
    return ;
}

float
MemPagerank::stop_one_iteration()
{
    std::swap(_pagerank, _target);
    float accumulated_diff = 0.0f;
    for (int i=0; i<_node_num; ++i) {
        accumulated_diff += fabs(_target[i] - _pagerank[i]);
        _target[i] = (1.0f - _damp) / (_node_num);
        
        // debug.
        fprintf(stderr, "node [%d] pr : %.4f\n", i, _pagerank[i]);
    }
    return accumulated_diff;
}

void 
MemPagerank::process_edge(const std::string& label_A, 
                const std::string& label_B, 
                float prob)
{
    size_t ia = label_to_id(label_A);
    size_t ib = label_to_id(label_B);
    if (_pagerank==NULL || _target==NULL || _node_num<=ia || _node_num<=ib) {
        throw std::logic_error("Cannot process edge.");
    }
    float flow = _damp * prob * _pagerank[ia];
    _target[ib] += flow;
    return ;
}

void
MemPagerank::dump_all(FILE* fp) const {
    for (std::map<std::string, size_t>::const_iterator it=_label_id_dict.begin();
            it!=_label_id_dict.end(); ++it)
    {
        fprintf(fp, "%s\t%.4f\n",
            it->first.c_str(),
            _pagerank[it->second]);
    }
}

//---------------------------------------------------------------------
struct Edge {
    std::string a;
    std::string b;
    float  prob;
};

int main ()
{
    // sample program.
    MemPagerank pagerank;

    std::vector<Edge> edge_list;
    // read edge from stdin.
    char line[1024 * 10];
    while (fgets(line, sizeof(line), stdin)) {
        size_t line_len = strlen(line);
        line[line_len --] = 0;

        Edge edge;
        std::vector<const char*> fields;
        fields.push_back(line);
        for (int i=0; i<line_len; ++i) {
            if (line[i] == '\t') {
                line[i] = 0;
                fields.push_back(line +i +1);
            }
        }
        if (fields.size()!=3) {
            fprintf(stderr, "Invalid line, fields num!=3\n");
        } else {
            edge.a = fields[0];
            edge.b = fields[1];
            edge.prob = atof(fields[2]);
            edge_list.push_back(edge);

            pagerank.add_node(edge.a);
            pagerank.add_node(edge.b);
        }
    }

    fprintf(stderr, "Read file over.\n");
    // begin iteration.
    pagerank.begin_iteration();

    // iteration.
    int iter_time = 0;
    while (1) {
        iter_time ++;
        // for each edge to process.
        for (int i=0; i<edge_list.size(); ++i) {
            Edge e = edge_list[i];
            pagerank.process_edge(e.a, e.b, e.prob);
        } 

        // need to stop one iteration.
        float acc = pagerank.stop_one_iteration();
        fprintf(stderr, "Step %d, accumulated_diff: %.4f\n", iter_time, acc);
        if (acc < 1e-4) {
            break;
        }
    }
    fprintf(stderr, "process over.\n");

    pagerank.dump_all(stdout);
}

/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
