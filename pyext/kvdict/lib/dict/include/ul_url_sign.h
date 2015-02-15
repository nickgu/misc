/* -*- c++ -*- 
   copy[write] by dirlt(dirtysalt1987@gmail.com) */
#ifndef _UL_URL_SIGN_H_
#define _UL_URL_SIGN_H_


/**
 * @brief calc 64bit site sign & 64bit url sign for a url string
 *
 * @param [in] urlstr   : const char*  null terminated url string
 * @param [out] site_sign   : unsigned long long& 
 * @param [out] url_sign   : unsigned long long&
 * @return  int  0 on sucess -1 on failure
 * @author liuchengcheng
 * @date 2010/07/05 14:38:14
 **/
//对urlstr进行归一化,然后使用murmurhash来计算site和url的签名.
//这里site_sign[0]和url_sign[0]为高32位,site_sign[1]和url_sign[1]为低32位.
int create_url_sign(const char *urlstr,unsigned int site_sign[2],unsigned int url_sign[2]);
int create_url_sign(const char* urlstr, unsigned long long& site_sign, unsigned long long& url_sign);


//下面两个函数和上面两个函数功能相同
//不过在处理url方面,支持了下面这样的url
//http://6wq-.blog.sohu.com/106289.html
//即在.之前允许-存在这样的url.而create_url_sign对于这样的url会报错.
//为pssearcher刘成城提供20101026.
//需要配合ullib3.1.37.0或者是更高版本使用.
int create_url_sign2(const char *urlstr,unsigned int site_sign[2],unsigned int url_sign[2]);
int create_url_sign2(const char* urlstr, unsigned long long& site_sign, unsigned long long& url_sign);

#endif
