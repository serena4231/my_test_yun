#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from btbase import bt
from base.dumbase import base
import time
def main():
#SETUP
    try:
        base.unlock()
        base.setup()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)

#enable and disable bluetooth
    try:
        base.find_setting()
        bt.enable_bt()
        time.sleep(1)
        bt.start_scanner()
        bt.stop_scanner()
    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     base.exit_app()