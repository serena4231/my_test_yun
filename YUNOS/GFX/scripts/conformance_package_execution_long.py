#!usr/bin/env python
#coding:utf-8
from base.baseflash import Command
import time
from base.logger import logger
import re

command_list=[r'adb -host remount',r'adb -host push /home/buildbot/conformance/ /data/',r'adb -host shell "cd /data/cts_foryunhal;chmod 777 conform"'
,r'adb -host shell "cd data/cts_foryunhal;./conform > result.log 2>&1"',]

def check_testrun():
    states,out,error=Command('adb -host shell cat /data/cts_foryunhal/result.log').start()
    search = re.compile('Test run 29 / 29')
    d=search.findall(out)
    if d ==[]:
        raise Exception('cannot find matched content')

    else:
        logger.info('keyword matched in file')

def main():
    stauts = True
    try:
        for i in command_list:
            Command(i).start()
            logger.info(i)
        check_testrun()
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts


main_test= main()
if main_test == True:
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE