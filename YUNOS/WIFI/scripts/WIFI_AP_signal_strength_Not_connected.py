#!usr/bin/env python
#coding:utf-8
from wifibase_version1 import wifi
from base.dumbase import base
from base.logger import logger
import time
def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        wifi.wifi_setup()
        wifi.check_singal('text="强"')
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


