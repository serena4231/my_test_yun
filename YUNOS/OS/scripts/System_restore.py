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

    except Exception,msg:
        logger.debug('Set_up_FAILED:%s'%msg)

     #system_restore
    try:
        BaseAPI().recover_system()
        time.sleep(120)
    except Exception,msg:
        logger.debug('system_restore_Exception:%s'%msg)

    ### tear down
    try:
        BaseAPI().setting_afterflash()
        BaseAPI().unlock()
        BaseAPI().setup()
        BaseAPI().back()
    except Exception,msg:
        logger.debug('Tear_down_Exception:%s'%msg)

try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
    VERDICT = FAILURE
finally:
     BaseAPI().exit_app()
