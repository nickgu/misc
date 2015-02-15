#!/usr/bin/python
#This is an simple example for MergeLog Parser(read from Protobuf Data)

import os.path
import sys

hadoop_home_path = "/home/work/gusimiu/hadoop-client/hadoop-client-stoff/hadoop"
hadoop_streaming_file = "ustreaming"

inputpath = ('hdfs://szwg-rank-hdfs.dmop.baidu.com:54310/app/ps/rank/ubs/mergelog-v2/mergelog-out/20140513/2[123]/part-*-A,'
            + 'hdfs://szwg-rank-hdfs.dmop.baidu.com:54310/app/ps/rank/ubs/mergelog-v2/mergelog-out/20140514/0*/part-*-A,' 
            + 'hdfs://szwg-rank-hdfs.dmop.baidu.com:54310/app/ps/rank/ubs/mergelog-v2/mergelog-out/20140514/1[0-7]/part-*-A' )
outputpath = '/ps/ubs/gusimiu/merge_0513'

#delete all the exist tmp result
command = hadoop_home_path + "/bin/hadoop dfs -rm "+outputpath+"/*"
os.system(command)
command = hadoop_home_path + "/bin/hadoop dfs -rmr " + outputpath
os.system(command)
print '**************************\n'

#generate the query log
command =  hadoop_home_path+"/bin/hadoop " + hadoop_streaming_file + \
        " -input " + inputpath +\
        " -output " + outputpath + \
        " -mapinstream binary" +\
        " -mapper \"./Python/Python/bin/python parser_demo.py\" " +\
        " -reducer \"cat\" " + \
        " -file " + "parser_demo.py" +\
        " -file " + "log_parser.so" +\
        " -file disp_rec_url.txt " + \
        " -cacheArchive /ps/ubs/gusimiu/upload/zhixin-python-2.7.3.tar#Python" + \
        " -inputformat org.apache.hadoop.mapred.SequenceFileAsBinaryInputFormat" +\
        " -jobconf mapred.reduce.tasks=1" +\
        " -jobconf mapred.job.name=\"gsm_test_mergelog\"" +\
        " -jobconf mapred.job.priority=VERY_HIGH"
print command,'\n'

os.system(command)
