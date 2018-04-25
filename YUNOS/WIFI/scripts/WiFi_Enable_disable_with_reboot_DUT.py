#!usr/bin/env python
#coding:utf-8
from wifibase_version1 import wifi
from base.dumbase import base
from base.logger import logger
from BT.scripts.btbase import bt
import time
def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        wifi.wifi_setup()
        base.reboot_version1()
        base.unlock()

        wifi.diconnect_check_enable()
        wifi.disable_wifi()
        base.reboot_version1()
        base.unlock()
        wifi.diconnect_check_disable()
        base.exit_app()

      ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
         wifi.wifi_setup()
         base.exit_app()
    return stauts



main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE

