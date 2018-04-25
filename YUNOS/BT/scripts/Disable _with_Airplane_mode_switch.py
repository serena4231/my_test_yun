#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import BaseAPI
from btbase import BTbase

import time
#SETUP
#. Enter the DUT  setting，enter the Bluetooth setting，disable Bluetooth
def main():
    try:
        BaseAPI().unlock()
        BaseAPI().setup()
        BaseAPI().find_setting()
        BTbase().disable_airplane()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)

#Turn on the airplane mode and Turn off  the airplane mode
#
    try:
        BaseAPI().find_setting()
        BTbase().disable_bt()
        time.sleep(1)
        BaseAPI().back()
        BTbase().enable_airplane()
        status = BTbase().bt()
        if status == False:
            logger.info('BT is still closed')

            BaseAPI().back()
            time.sleep(1)
            BTbase().disable_airplane()
            status = BTbase().bt()
            if status == False:
                logger.info('Success:closed the airplane, The bluetooth is still closed')
                BaseAPI().back()
            else:
                logger.debug('Failed:closed the airplane, The bluetooth is opened')
                exit(1)
        else:
            logger.debug('Failed:opened the airplane mode, bluetooth is opened')
            exit(1)

    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
    VERDICT = FAILURE
finally:
        BaseAPI().exit_app()


