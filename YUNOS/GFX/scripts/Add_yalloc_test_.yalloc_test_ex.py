#!/usr/bin/env python
#coding:utf-8
from base.dumbase import base
import re
from base.dumbase import Command
from base.dumbase import logger
from base.dumbase import checkfile
import time
def check_result(args):
    find = re.compile('PASSED')
    d=find.search(args)
    if d ==[]:
        raise Exception('yalloc test is failed')
    else:
        logger.info('yalloc test is success')

def main():
    status = True
    try:
        base.unlock()
        base.setup()
        states,out1,error= Command('adb -host shell yalloc_test_ex').start()
        check_result(out1)
        time.sleep(5)
        states,out2,error = Command('adb -host shell yalloc_test').start()
        check_result(out2)
        time.sleep(30)
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        status = False
    return status

main_test = main()
if main_test == True:
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE

