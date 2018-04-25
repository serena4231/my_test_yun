#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import BaseAPI
from btbase import BTbase

import time
#SETUP
#Enter the DUT  setting，enter the Bluetooth setting，enable Bluetooth.
def main():
    try:

        BaseAPI().unlock()
        BaseAPI().setup()
        i = 0
        while i <30:
            BaseAPI().find_setting()
            BTbase().disable_airplane()

    ##Turn on the airplane mode and Turn off  the airplane mode
            BaseAPI().find_setting()
            BTbase().enable_bt()
            time.sleep(1)
            BaseAPI().back()
            BTbase().enable_airplane()
            status = BTbase().bt()
            if status == True:
                logger.info('BT is still opened')
                logger.debug('open the airplane, cannot disable the bluetooth')
                exit(1)
            else:
                BaseAPI().back()
                time.sleep(1)
                BTbase().disable_airplane()
                status = BTbase().bt()
                if status == True:
                    logger.info('closed the airplane, opened the bluetooth is success')
                    BaseAPI().back()
            BaseAPI().exit_app()
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