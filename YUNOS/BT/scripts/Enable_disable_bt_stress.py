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

#enable and disable bluetooth
    try:
        BaseAPI().find_setting()
        i = 0
        while i <30:
            BTbase().enable_bt()
            BTbase().disable_bt()
            i+=1

    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     BaseAPI().exit_app()