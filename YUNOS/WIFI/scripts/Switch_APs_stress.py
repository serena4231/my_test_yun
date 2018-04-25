#!usr/bin/env python
#coding:utf-8
from wifibase_version1 import wifi
from base.dumbase import base
from base.dumbase import checkfile
from base.logger import logger
from base.dumbase import Command
import time
def switch_ap():
    wifi.connect_wifi('text="YUNOS_Auto_Test_2G"')
    time.sleep(1)
    wifi.swtich_ap_connect('text="YUNOS_Auto_Test_5G"')
    wifi.check_ap_status()
    checkfile.click('text="YUNOS_Auto_Test_2G"')
    time.sleep(5)
    checkfile.click('text="YUNOS_Auto_Test_5G"')
    time.sleep(5)
def discon_wifi():
    count = 0
    while count<2:
        time.sleep(2)
        Command('adb -host shell input longtap 200 180').start()
        time.sleep(3)
        Command('adb -host shell input longtap 270 580').start()
        time.sleep(5)
        count+=1
    base.exit_app()

def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        i = 0
        while i <50:
            wifi.wifi_setup()
            switch_ap()
            discon_wifi()
            i+=1
            logger.info('stress times is %d'%i)
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

