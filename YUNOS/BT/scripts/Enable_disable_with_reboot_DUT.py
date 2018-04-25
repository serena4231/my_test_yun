#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from btbase import BTbase


import time
#SETUP
#Enter the DUT  setting，enter the Bluetooth setting，enable Bluetooth.
def main():
    try:
        base.unlock()
        base.setup()
        base.find_setting()
        BTbase().enable_bt()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)


#Reboot the DUT,enter the Bluetooth setting
    try:
        base.setting_reboot_version1()
        newstatus =BTbase().bt()
        if newstatus== False:
            logger.debug('bluetooth is closed after reboot ')
            exit(1)
        else:
            BTbase().disable_bt()
            base.setting_reboot_version1()
            newstatus =BTbase().bt()
            if newstatus == False:
                logger.info('Success:bluetooth still is closed')


            else:
                logger.debug('Failed:bluetooth is opened')
                exit(1)
    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
    base.exit_app()





