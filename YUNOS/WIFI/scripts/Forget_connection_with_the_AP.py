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
        wifi.connect_wifi('YUNOS_Auto_Test_2G')
        base.back()
        wifi.disconnect_wifi('YUNOS_Auto_Test_2G')
        wifi.connect_wifi('YUNOS_Auto_Test_2G')

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



