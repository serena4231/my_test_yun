#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from btbase import bt
import time

def enable_disable_scan(count):
    i = 0
    while i < count:
        bt.enable_bt()
        time.sleep(1)
        bt.start_scanner()
        bt.disable_bt()
        i +=1
        logger.info("enable and disable bluetooth during scanning try: %d" %(i))


def main():
#SETUP
    try:
        base.unlock()
        base.setup()

#enable and disable bluetooth
        base.find_setting()
        enable_disable_scan(10)

    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     base.exit_app()
