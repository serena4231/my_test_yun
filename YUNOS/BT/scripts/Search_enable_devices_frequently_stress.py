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

        base.find_setting()
        bt.enable_bt()
        time.sleep(1)
        for i in range(10):
            bt.start_discovery()
            time.sleep(1)
            bt.stop_discovery()
            time.sleep(1)
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