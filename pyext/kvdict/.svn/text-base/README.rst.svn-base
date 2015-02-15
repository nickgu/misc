KVDict
======

应用背景
--------
主要为了解决python词典占用内存过大的问题
适用用一下几种情况::
    * 将一个文本按照第一列为key，后面为value的方式读入内存。
    * 同样是这样的文件，不读入内存，只是建立一个索引

使用方法
--------
可以参考kvdict.py中使用方法。主要有几种情况：

    创建词典:
       import kvdict
       # 创建一个内存词典
       dct = kvdict.KVDict()
       # 创建一个文件索引词典
       idx_dct = kvdict.FileIndexKVDict()

    读取文件
        dct.load(filename)
        dct.load([filenameA, filenameB, filenameC])
        idx_dct.load(filename)
        idx_dct.load([filenameA, filenameB, filenameC])

    查询
        ret = dct.find(key)
        # or
        # ret = idx_dct.find(key)
        if ret is None:
            # not found.
            pass
        else:
            # found.

    序列化内存词典（加速下次读取）
        dct.dump_bin(output_filename)
        dct.load_bin(input_filename)

