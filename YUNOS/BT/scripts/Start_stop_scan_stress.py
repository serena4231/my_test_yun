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

        base.find_setting()
        bt.enable_bt()
        time.sleep(1)
        i = 0
        while i<30:
            bt.start_scanner()
            time.sleep(3)
            bt.stop_scanner()
            time.sleep(3)
            logger.info('try time is %d'%i)
            i+=1
    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     base.exit_app()