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

#discovery and no discovery
        i = 0
        while i <10:
            base.find_setting()
            bt.enable_bt()
            time.sleep(1)
            bt.start_discovery()
            time.sleep(1)
            bt.disable_bt()

            #######
            bt.enable_bt()
            bt.check_scanner()
            bt.stop_discovery()
            bt.disable_bt()
            ######
            bt.enable_bt()
            bt.stop_discovery()
            base.exit_app()
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
