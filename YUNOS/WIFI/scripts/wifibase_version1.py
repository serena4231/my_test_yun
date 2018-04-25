#!/usr/bin/env python
#coding:utf-8


from base.baseflash import Command
from base.logger import logger
import time
from base.dumbase import checkfile
from base.dumbase import base
import re


WIFI_Comm={'LANCH_WIFI':'adb -host shell input tap 60 130',
           'SWITCH_WIFI_STATUS':'adb -host shell input tap 60 90',
           'PASSWORD':'adb -host shell input text 12345678',
           'SELECT_RITHT':'adb -host shell input tap 950 50',
           'STATIC':'adb -host shell input tap 500 460',
           'IPV4_ADDRESS':'adb -host shell input tap 900 390',
           'IPV4_INPUT':'adb -host shell input text "192.168.1.100"',




}
import shutil

class Wifibase():
    def launch_wifi(self):
        base.find_setting()
        Command(WIFI_Comm['LANCH_WIFI']).start()
        time.sleep(1)
        status =checkfile.check_stauts('checked="true"')
        if status == False:
            Command(WIFI_Comm['SWITCH_WIFI_STATUS']).start()
            time.sleep(2)
            new_stauts = checkfile.check_stauts('text="WLAN 列表"')
            if new_stauts == False:
                raise Exception('launch wifi is failed')
        else:
            logger.info('launch wifi is success')
    def check_connect_disable(self):
        Command(WIFI_Comm['LANCH_WIFI']).start()
        time.sleep(2)
        status = checkfile.check_stauts('text="已连接"')
        if status == False:
            logger.info('disable connect is success')
            base.back()
        else:
            raise Exception('disable connect is failed')
    def check_connect_enable(self):
        Command(WIFI_Comm['LANCH_WIFI']).start()
        time.sleep(2)
        status = checkfile.check_stauts('text="已连接"')
        if status == True:
            logger.info('enable connect is success')
            base.back()
        else:
            raise Exception('enable connect is failed')

    def connect_wifi(self,args):
        status = checkfile.check_stauts('text="已连接"')
        if status == False:
            time.sleep(2)
            checkfile.click(args)
            time.sleep(2)
            Command(WIFI_Comm['PASSWORD']).start()
            time.sleep(2)
            checkfile.long_click('text="确定"')
            # Command(WIFI_Comm['SELECT_RITHT']).start()
            time.sleep(10)
            status=checkfile.check_stauts('text="已连接"')
            if status == False:
                raise Exception('connect the wifi is failed')
            else:
                logger.info('connect the wifi is success')
        else:
            logger.info('Connect the wifi is success')
    def swtich_ap_connect(self,args):
        checkfile.click(args)
        time.sleep(2)
        Command(WIFI_Comm['PASSWORD']).start()
        time.sleep(2)
        checkfile.click('text="确定"')
        time.sleep(10)
        status=checkfile.check_stauts('text="已连接"')
        if status == False:
            raise Exception('connect the wifi is failed')
        else:
            logger.info('connect the wifi is success')
    def check_ap_status(self):
        status = checkfile.check_stauts('text="已保存"')
        if status == False:
            raise Exception('switch AP is failed')
        else:
            logger.info('switch AP is success')


    def disconnect_wifi(self,args):
        count = 0
        self.launch_wifi()
        while count < 3:
            time.sleep(2)
            checkfile.long_click(args)
            time.sleep(1)
            status=checkfile.check_stauts('text="取消保存"')
            if status == False:
                logger.info('try more one times %d'%count)
                count+=1
                time.sleep(1)
            else:
                time.sleep(1)
                checkfile.click('text="取消保存"')
                logger.info('disconnect is success')
                break
    def check_info(self):
        Command('adb -host shell input longtap 60 180').start()
        status=checkfile.check_stauts('text="详细信息"')
        if status == True:
            time.sleep(2)
            Command('adb -host shell input tap 100 630').start()
            logger.info('check the wlan info')

    def enable_wifi(self):
        time.sleep(1)
        status =checkfile.check_stauts('checked="true"')
        if status == False:
            time.sleep(3)
            checkfile.click('checked="false"')
            time.sleep(10)
            new_status = checkfile.check_stauts('checked="true"')
            if new_status == False:
                raise Exception('enable wifi is failed')
            else:
                logger.info('enable wifi is success')
        else:
            logger.info('wifi is enabled')
    def diconnect_check_enable(self):
        base.unlock()
        base.find_setting()
        Command(WIFI_Comm['LANCH_WIFI']).start()
        time.sleep(1)
        status =checkfile.check_stauts('checked="true"')
        if status == False:
            raise Exception('enable wifi status is failed')
        else:
            logger.info('enable wifi status is success')
    def diconnect_check_disable(self):
        base.unlock()
        base.find_setting()
        Command(WIFI_Comm['LANCH_WIFI']).start()
        time.sleep(1)
        status =checkfile.check_stauts('checked="true"')
        if status == True:
            raise Exception('enable wifi status is failed')
        else:
            logger.info('enable wifi status is success')

    def disable_wifi(self):
        status =checkfile.check_stauts('checked="false"')
        if status == False:
            checkfile.click('checked="true"')
            time.sleep(1)
            new_status = checkfile.check_stauts('checked="false"')
            if new_status == False:
                raise Exception('disable wifi is failed')
            else:
                logger.info('disable wifi is success')
        else:
            logger.info('wifi is enabled')

    def change_ipv4(self):
        self.check_info()
        time.sleep(2)
        # checkfile.click('text="高级选项"')
        # time.sleep(1)
        checkfile.click('text="IPv4设置"')
        time.sleep(1)
        ################静态
        # Command(WIFI_Comm['STATIC']).start()
        checkfile.click('text="静态"')
        time.sleep(1)
        ##########IPV4
        Command(WIFI_Comm['IPV4_ADDRESS']).start()
        base.longpress_delete()
        Command(WIFI_Comm['IPV4_INPUT']).start()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        time.sleep(10)
        status=checkfile.check_stauts('text="已连接"')
        if status == False:
            raise Exception('connect the wifi is failed')
        else:
            logger.info('connect the wifi is success')


    def change_ipv4_stress(self):
        self.check_info()
        time.sleep(2)
        # checkfile.click('text="高级选项"')
        # time.sleep(1)
        checkfile.click('text="IPv4设置"')
        time.sleep(1)
        ################静态
        # Command(WIFI_Comm['STATIC']).start()
        checkfile.click('text="静态"')
        time.sleep(1)
        ##########IPV4
        Command(WIFI_Comm['IPV4_ADDRESS']).start()
        base.longpress_delete()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        time.sleep(1)
        status=checkfile.check_stauts('text="子网掩码"')
        if status == True:
            base.longpress_delete()
            logger.info('detel one  input box ')
            Command('adb -host shell input text "130.112.1.100"')
            Command(WIFI_Comm['SELECT_RITHT']).start()
            status=checkfile.check_stauts('text="子网掩码"')
            if status == True:
                base.longpress_delete()
                Command('adb -host shell input tex "acv中"')
                new_stauts = checkfile.check_stauts('text="acv中""')
                if new_stauts == False:
                    logger.info('All test pass')
                else:
                    raise Exception('input int type reuslt is failed')
            else:
                raise Exception('input wrong ip result is failed')
        else:
            raise Exception('input null ip result is failed')
        base.longpress_delete()
        Command(WIFI_Comm['IPV4_INPUT']).start()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        time.sleep(10)
        status=checkfile.check_stauts('text="已连接"')
        if status == False:
            raise Exception('connect the wifi is failed')
        else:
            logger.info('connect the wifi is success')

    def check_ifconfig(self):
        Command('adb -host shell input longtap 60 180').start()
        status = checkfile.check_stauts('text="192.168.1.100"')
        if status == True:
            logger.info('ifconfig changed is success')
        else:
            raise Exception('ifconfig changed is failed')

    def add_hidden_ssd(self):
        Command('adb -host shell input swipe 900 700 900 100').start()
        checkfile.click('text="添加网络"')
        time.sleep(1)
        Command('adb -host shell input text "ITFLEX_YUNOS_H"').start()
        time.sleep(1)
        checkfile.click('text="安全性"')
        time.sleep(1)
        checkfile.click('text="PSK"')
        time.sleep(1)
        Command('adb -host shell input tap 600 300').start()
        Command('adb -host shell input text 12345678').start()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        time.sleep(10)
        base.back()
        self.check_connect_enable()
    def add_hidden_ssd_stress_mode(self):
        Command('adb -host shell input swipe 900 700 900 100').start()
        checkfile.click('text="添加网络"')
        time.sleep(1)
        Command('adb -host shell input text "ITFLEX_YUNOS_H"').start()
        time.sleep(1)
        checkfile.click('text="安全性"')
        time.sleep(1)
        #click security mode set wep
        checkfile.click('text="WEP"')
        Command('adb -host shell input tap 600 300').start()
        Command('adb -host shell input text 12345678').start()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        stauts = checkfile.check_stauts('text="网络名称"')
        if stauts == False:
            raise Exception('click security mode set WEP is failed')
        #click security mode set none
        time.sleep(1)
        checkfile.click('text="安全性"')
        checkfile.click('text="无"')
        time.sleep(1)
        Command(WIFI_Comm['SELECT_RITHT']).start()
        stauts = checkfile.check_stauts('text="已连接"')
        if stauts == True:
            raise Exception('click security mode set none is failed')
    def add_hidden_ssd_stress_wrongpw(self):
        Command('adb -host shell input swipe 900 700 900 100').start()
        checkfile.click('text="添加网络"')
        time.sleep(1)
        Command('adb -host shell input text "ITFLEX_YUNOS_H"').start()
        time.sleep(1)
        checkfile.click('text="安全性"')
        time.sleep(1)
        checkfile.click('text="PSK"')
        time.sleep(1)
        Command(WIFI_Comm['SELECT_RITHT']).start()
        stauts = checkfile.check_stauts('text="添加网络"')
        if stauts == False:
            raise Exception('add none password is failed')
        Command('adb -host shell input tap 600 300').start()
        Command('adb -host shell input text 123456').start()
        Command(WIFI_Comm['SELECT_RITHT']).start()
        stauts = checkfile.check_stauts('text="添加网络"')
        if stauts == False:
            raise Exception('add none password is failed')

    def check_singal(self,args):
        Command('adb -host shell input longtap 60 180').start()
        time.sleep(2)
        status = checkfile.check_stauts(args)
        if status == False:
            raise Exception('show signal strength is failed')
        else:
            logger.info('show signal strength is success')


    def wifi_setup(self):
        self.launch_wifi()
        self.enable_wifi()
    def wlan_info(self):
        Command(WIFI_Comm['LANCH_WIFI']).start()

# wifi=Wifibase()
