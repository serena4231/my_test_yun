#!usr/bin/env python
#coding:utf-8
from wifibase_version1 import wifi
from base.dumbase import base
from base.dumbase import checkfile
from base.logger import logger
import time
def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        wifi.wifi_setup()
        wifi.connect_wifi('text="YUNOS_Auto_Test_2G"')
        time.sleep(1)
        wifi.swtich_ap_connect('text="YUNOS_Auto_Test_5G"')
        wifi.check_ap_status()
        checkfile.click('text="YUNOS_Auto_Test_2G"')
        time.sleep(5)
        checkfile.click('text="YUNOS_Auto_Test_5G"')
        time.sleep(5)
        base.back()
  ##########################

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
        wifi.disconnect_wifi('YUNOS_Auto_Test_2G')
        base.back()
        wifi.disconnect_wifi('YUNOS_Auto_Test_5G')
        base.exit_app()
    print stauts
    return stauts



main_test = main()
if main_test == True :
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE