#!usr/bin/env python
#coding:utf-8
from base.baseflash import Command
import time
from base.logger import logger
import re
command_list=[r'adb -host remount',r'adb -host push /home/buildbot/conformance/ /data/',r'adb -host shell "cd /data/cts_foryunhal;chmod 777 conform"'
,r'adb -host shell "cd data/cts_foryunhal;./conform --runconfig=6 > result6.log 2>&1"',r'adb -host shell "cd data/cts_foryunhal;./conform --runconfig=25 > result25.log 2>&1"']
def check_testrun(args,testrun):
    states,out,error=Command('adb -host shell cat /data/cts_foryunhal/%s'%args).start()
    search = re.compile('Test run {} / 29'.format(testrun))
    d=search.findall(out)
    if d ==[]:
        raise Exception('%s cannot find matched content'%args)

    else:
	    logger.info('%s keyword matched in file'%args)


def main():
    stauts = True
    try:
        for i in command_list:
            Command(i).start()
            logger.info(i)
        check_testrun('result6.log','6')
        check_testrun('result25.log','25')
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts


main_test= main()
if main_test == True:
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE


