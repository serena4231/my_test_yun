#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from btbase import bt
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
        for i in range(5):
            bt.enable_bt()
            bt.disable_bt()
            logger.info('***********currently cycles is %d*************'%i)
        bt.enable_bt()
        time.sleep(50)
        bt.devices_discovery('resource-id')

    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     base.exit_app()
