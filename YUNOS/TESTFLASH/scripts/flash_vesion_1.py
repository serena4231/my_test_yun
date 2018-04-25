
#!usr/bin/env python
#coding:utf-8

import os
import time
from base.relay08 import Relayed_device
from base.baseflash import Command
from base.dumbase import base
from base.baseflash import check_adb_device
path = r'/home/buildbot/flashfile/flash'

cmd_list = [r'sudo fastboot boot loader.efi',r'sudo fastboot oem unlock',r'sudo fastboot flash gpt gpt.bin',r'sudo fastboot erase misc',r'sudo fastboot erase persistent',r'sudo fastboot erase metadata',
            r'sudo fastboot format config',r'sudo fastboot format cache',r'sudo fastboot flash boot boot.img',r'sudo fastboot flash system system.img',r'sudo fastboot flash bootloader bootloader',
            r'sudo fastboot oem verified',r'sudo fastboot format data',r'sudo fastboot continue']
def set_up():
    base.screen_on()
    base.unlock()
    base.setup()
    base.back()
def plugin_set():
    Command('adb -host remount').start()
    Command('adb -host shell mkdir -p /usr/var/arp/').start()
    Command('adb -host push arp.plg /usr/var/arp/arp.img').start()
    time.sleep(120)

def swtich_ARP():
    Command('adb -host shell sendlink page://installPluginDemo.yunos.com/installPluginDemo').start()
    Command('adb -host shell input tap 500 400').start()
    time.sleep(200)
    set_up()

def main():

    Command('sudo chmod 777 /dev/ttyRelayCard').start()
    #close devices
    relay_devices=Relayed_device('/dev/ttyRelayCard','65')
    relay_devices.power_off()
    relay_devices.write('6E')
    relay_devices.close()
    time.sleep(20)

    #start relycard
    relay_devices=Relayed_device('/dev/ttyRelayCard','65','69')
    #enter in dnx model
    relay_devices.enter_dnx()
    relay_devices.close()
    #close relay ports
    relay_devices=Relayed_device('/dev/ttyRelayCard','6f','73')
    relay_devices.close_dnx()
    relay_devices.close()
    #copy flash file
    # flashfile = Flashfile(path)
    # flashfile.extract_flash_file(os.path.join(path,'flash.zip'))
    #flash devices
    os.chdir(path)
    for i in cmd_list:
        print(i)
        Command(i).start(80)
    time.sleep(200)
    plugin_set()
    set_up()
    swtich_ARP()

try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
