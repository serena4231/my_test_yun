#!/usr/bin/env python
#coding:utf-8

from base.dumbase import BaseAPI
import time
from base.logger import logger

def main():
    #SETUP
    try:
        BaseAPI().unlock()
        BaseAPI().setup()
        BaseAPI().recover_system_new()
        time.sleep(300)
    ### tear down
        BaseAPI().screen_on()
        BaseAPI().unlock()
        BaseAPI().setup()
    except Exception,msg:
        logger.debug('Tear_down_Exception:%s'%msg)

try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
    VERDICT = FAILURE
finally:
     BaseAPI().exit_app()

