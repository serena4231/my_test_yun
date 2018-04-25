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
        wifi.disable_wifi()
        base.back()
        bt.enable_airplane()
        time.sleep(10)
        wifi.check_connect_disable()
        bt.disable_airplane()
        time.sleep(10)
        wifi.check_connect_disable()
      ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
         base.exit_app()
    return stauts



main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE

