#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import BaseAPI
from btbase import BTbase

def main():
#SETUP
    try:
        BaseAPI().unlock()
        BaseAPI().setup()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)

#Change the adapter name.
    try:
        BaseAPI().find_setting()
        BTbase().enable_bt()
        BTbase().change_adapter_name('PEACOCK','YUNOS','测试1')
        BTbase().revert_adapter_name()

    except Exception,msg:
        logger.debug('Exception:%s'%msg)

try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     BaseAPI().exit_app()
