#!/usr/bin/env python
#coding:utf-8

from base.baseflash import Command
from base.logger import logger
from base.dumbase import checkfile
import re
from base.dumbase import BaseAPI
from base.dumbase import base
import time
from base.checkcrash import check_system


BT_Comm={
    'OPENSETTING':'adb -host shell sendlink "page://settings.yunos.com/settings"',
    'BT': 'adb -host shell input tap 68 199',
    'SWTICH_BT':'adb -host shell input tap 1230 92',
    'SWTICH_SEACH':'adb -host shell input tap 1232 161',#开放检测开关
    'AIRPLANEMODE':'adb -host shell input tap 110 260',
    'CHANGE_ADAPTER_NAME':'adb -host shell input tap 99 260',
    'DEVICE_NAME':'adb -host shell input tap 600 400',
    'KEYIN_DEVICENAME':'adb -host shell input text PEACOCK',
    'ENSURE_CHANGENAME_BUTTON':'adb -host shell input tap 650 443',
    'DISCOVERY':'adb -host shell input tap 560 740',
    'SCANNER':'adb -host shell input tap 100 160'
}

#Enable/Disable BT
class BTbase():

    def bt(self):
        Command(BT_Comm['BT']).start()
        time.sleep(1)
        status =checkfile.check_stauts('开放检测')
        return status
    def enable_bt(self):

        status = self.bt()
        if status == False:
            logger.info('need to open the bluetooth')
            Command(BT_Comm['SWTICH_BT']).start(10)
            new_status = checkfile.check_stauts('text="点击更改设备名称"')
            if new_status == True:
                logger.info('running to open the bluetooth')
            else:
                raise Exception('cannot open the bluetooth')

        else:
            logger.info('opened bluetooth')

    def check_scanner(self):
        status=checkfile.check_stauts('resource-id="ali_key_bluetooth_available_device_list"')
        if status == False:
            raise Exception('start scan is Failed')

    def disable_bt(self):
        status = self.bt()
        if status == True:
            logger.info('need to close the bluetooth')
            Command(BT_Comm['SWTICH_BT']).start()
            time.sleep(2)
            new_status = checkfile.check_stauts('text="打开蓝牙，搜索可用设备"')
            if new_status == True:
                logger.info(' running to close the bluetooth')
            else:
                raise Exception('cannot close the bluetooth')

        else:
            logger.info('bluetooth is closed')

    def enable_airplane(self):
        status=checkfile.check_stauts('checked="false"')
        if status == True:
            logger.info('need to open the airplane')
            Command(BT_Comm['AIRPLANEMODE']).start()
            time.sleep(1)
            new_status = checkfile.check_stauts('checked="false"')
            if new_status == False:
                logger.info('running to open the airplane')
            else:
                raise Exception('cannot open the airplane')
        else:
            logger.info('opened airplane')
    def disable_airplane(self):
        status=checkfile.check_stauts('checked="true"')
        if status == True:
            logger.info('need to close the airplane')
            Command(BT_Comm['AIRPLANEMODE']).start()
            time.sleep(1)
            new_status = checkfile.check_stauts('checked="true"')
            if new_status == False:
                logger.info('running to close the airplane')
            else:
                raise Exception('cannot close the airplane')
        else:
            logger.info('closed airplane')


    def click_adapter_name(self):
        try:
            checkfile.check_stauts('text="点击更改设备名称"')
            Command(BT_Comm['CHANGE_ADAPTER_NAME']).start()
            time.sleep(1)
            Command(BT_Comm['DEVICE_NAME']).start()
            BaseAPI().longpress_delete()
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)

    def change_adapter_name(self,*args):
        try:
            for i in args:
                self.click_adapter_name()

                Command('adb -host shell input text {0}'.format(i)).start()
                # Command(BT_Comm['KEYIN_DEVICENAME']).start()
                Command(BT_Comm['ENSURE_CHANGENAME_BUTTON']).start()
                time.sleep(1)
                stauts =checkfile.check_stauts('text="{0}"'.format(i))
                if stauts == True:
                    logger.info('SUCESS:finished the change adapter name')
                else:
                    raise Exception('FAIL:change the adapter occur with issue')
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)
    def check_adapter_name(self,args):
        status = checkfile.check_stauts(args)
        if status == True:
                logger.info('adapter name is right')
        else:
            raise Exception('adapter name is wrong')


    def revert_adapter_name(self):
        try:
            self.click_adapter_name()
            Command('adb -host shell input text Peacock').start()
            time.sleep(1)
            Command(BT_Comm['ENSURE_CHANGENAME_BUTTON']).start()
            time.sleep(1)
            stauts =checkfile.check_stauts('text="Peacock"')
            if stauts == True:
                logger.info('SUCESS:finished the revert adapter name')
            else:
                raise Exception('FAIL:revert the adapter occur with issue')
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)

    def start_scanner(self):
        stauts=checkfile.check_stauts('text="附近所有的蓝牙设备均可检测到此设备"')
        if stauts == False:
            status,output,error=Command(BT_Comm['SCANNER']).start()
            base.check_adb_command('ret = true',output)
            result = check_system.check_test_result('page://settings.yunos.com')
            if result == False:
                raise Exception('start discovery occur with issues')
        logger.info('close scanner is success')
    def stop_scanner(self):
        stauts=checkfile.check_stauts('text="附近所有的蓝牙设备均可检测到此设备"')
        if stauts == True:
            status,output,error=Command(BT_Comm['SCANNER']).start()
            base.check_adb_command('ret = true',output)
            result = check_system.check_test_result('page://settings.yunos.com')
            if result == False:
                raise Exception('start discovery occur with issues')
        logger.info('open scanner is success')

    def start_discovery(self):
        time.sleep(1)
        status=checkfile.check_stauts('text="停止搜索"')
        if status == False:
            Command(BT_Comm['DISCOVERY']).start()
            logger.info('*********start discovery************')
            result = check_system.check_test_result('page://settings.yunos.com')
            if result == False:
                raise Exception('start discovery occur with issues')

    def stop_discovery(self):
        time.sleep(1)
        status=checkfile.check_stauts('text="停止搜索"')
        if status == True:
            Command(BT_Comm['DISCOVERY']).start()
            logger.info('**********stop discovery********')
            result = check_system.check_test_result('page://settings.yunos.com')
            if result == False:
                raise Exception('start discovery occur with issues')
    def devices_discovery(self,args):
        checkfile.create_dump()
        states,f,error=Command('adb -host shell cat /var/log/uidump.txt').start()
        lunum = 0

        for line in f.splitlines():
            lunum +=1
            if (lunum >= 102)& (lunum <=130):
                print line
                searach = re.compile(args)
                d= searach.findall(line)
                if d == []:
                    pass
                else:
                    raise Exception('Cannot serach any bluetooth devices')


bt = BTbase()
