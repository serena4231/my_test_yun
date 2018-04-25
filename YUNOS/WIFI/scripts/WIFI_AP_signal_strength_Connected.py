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
        wifi.connect_wifi('text="YUNOS_Auto_Test_2G"')
        wifi.check_singal('text="强"')
        base.exit_app()
  ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
        wifi.disconnect_wifi('text="YUNOS_Auto_Test_2G"')
        base.exit_app()
    return stauts



main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FA