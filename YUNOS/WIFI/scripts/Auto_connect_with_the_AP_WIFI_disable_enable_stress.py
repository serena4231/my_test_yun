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
        wifi.connect_wifi('YUNOS_Auto_Test_2G')
        for i in range(50):
            wifi.disable_wifi()
            time.sleep(5)
            wifi.enable_wifi()
            time.sleep(5)
            base.back()
            time.sleep(10)
            wifi.check_connect_enable()
            time.sleep(2)
            wifi.wlan_info()

            logger.info('************stress times is************ %d'%i)


  ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
        base.back()
        wifi.disconnect_wifi('YUNOS_Auto_Test_2G')
        base.exit_app()

    return stauts

main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE


