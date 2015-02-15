
#ifndef __HELPER_H__
#define __HELPER_H__

#include <ctime>

#include <vector>
#include <string>
#include <stdexcept>

#include <sys/time.h>

#ifndef LOG_NOTICE
#define LOG_NOTICE(format, ...) {fprintf(stderr, "NOTICE: " format "\n", ##__VA_ARGS__);}
#endif 

#ifndef LOG_ERROR
#define LOG_ERROR(format, ...) {fprintf(stderr, " ERROR: " format "\n", ##__VA_ARGS__);}
#endif


class Timer {
public:
    Timer() :_sum(0.0) {}

    void begin() {
        gettimeofday(&_begin_tv, NULL);
    }

    void end() {
        gettimeofday(&_end_tv, NULL);
        _sum += (_end_tv.tv_sec - _begin_tv.tv_sec) + (_end_tv.tv_usec - _begin_tv.tv_usec) * 0.000001f;
    }

    /* return unit : seconds.*/
    float cost_time() const {
        return _sum;
    }

private:
    float   _sum;

    timeval _begin_tv;
    timeval _end_tv;
};

template <typename T>
class FArray_t {
    public:
        FArray_t(size_t extend_num=512):
            _l(NULL),
            _num(0),
            _bnum(0),
            _extend_num(extend_num),
            _magic_check(0xDEADBEEF)
        {}

        FArray_t(const FArray_t& o) {
            *this = o;
        }

        FArray_t& operator = (const FArray_t& o) {
            _release();
            _bnum = o._bnum;
            _num = o._num;
            _extend_num = o._extend_num;
            if (_bnum > 0) {
                _l = (T*)malloc(_bnum * sizeof(T));
                //LOG_NOTICE("m: %p [%u]", _l, _bnum);
                memcpy(_l, o._l, _num * sizeof(T));
            }
            return *this;
        }

        ~FArray_t() { _release(); }

        size_t size() const {return _num;}

        void push_back(const T& o) {
            if (_num == _bnum) {
                _extend();
            }
            _l[_num ++] = o;
        }

        void clear() { _num = 0; }

        T& operator [] (size_t idx) {
            if (idx >= _num) {
                throw std::runtime_error("index out of range.");
            }
            return _l[idx];
        }
        T& operator [] (size_t idx) const {
            if (idx >= _num) {
                throw std::runtime_error("index out of range.");
            }
            return _l[idx];
        }


    private:
        T *_l;
        size_t _num;
        size_t _bnum;
        size_t _extend_num;
        unsigned _magic_check;

        void _extend() {
            _l = (T*)realloc(_l, (_bnum + _extend_num) * sizeof(T) );
            //LOG_NOTICE("r: %p", _l);
            if (_l == NULL) {
                throw std::runtime_error("extend buffer for FArray failed!");
            }
            _bnum += _extend_num;
        }

        void _release() {
            if (_magic_check == 0xDEADBEEF) {
                // do nothing because in glib, a new on wild memory will happen.
                // which leads to a exception free.
                if (_l) {
                    free(_l);
                }
            }
            _l = NULL;
            _num = _bnum = 0;
        }
};

void split(char* s, const char* token, std::vector<std::string>& out) {
    char* p;
    out.clear();
    char* f = strtok_r(s, token, &p);
    while (f) {
        out.push_back(f);
        f = strtok_r(NULL, token, &p); 
    }
    return ;
}


#endif
