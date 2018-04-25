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
        wifi.swtich_ap_connect('text="YUNOS_Auto_Test_5G"')
        time.sleep(5)
        wifi.check_ap_status()
        base.back()
        wifi.disconnect_wifi('text="YUNOS_Auto_Test_5G"')
  ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
        base.exit_app()
        base.find_setting()
        wifi.disconnect_wifi('text="YUNOS_Auto_Test_2G"')
        base.exit_app()
    return stauts



main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE
