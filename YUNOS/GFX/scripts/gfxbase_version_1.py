#!/usr/bin/env python
#coding:utf-8

from WIFI.scripts.wifibase import wifi
from base.dumbase import base
from base.baseflash import Command
from base.dumbase import checkfile
from base.logger import logger

import time
#vesrion6.1 app address:page://ucbrowser.yunos.com/browser
#version6.0 app address:page://browser.yunos.com/browser
GFX_Comm={'LANCH_BROWSE':'adb -host shell sendlink page://ucbrowser.yunos.com/browser',
          'ADDRESS_3':'adb -host shell input text http://ie.microsoft.com/testdrive/Performance/FishBowl/',
          'ADDRESS_2':'adb -host shell input text http://www.smashcat.org/av/canvas_test/',
          'ADDRESS_1':'adb -host shell input text http://kevs3d.co.uk/dev/canvask3d/k3d_test.html',
          'ADDRESS_4':'adb -host shell input text http://www.kevs3d.co.uk/dev/canvasmark/',
          'START_4':'adb -host shell input tap 100 160'
}

class Gfxbase():
    def set_up(self,args):
        base.unlock()
        base.setup()
        wifi.launch_wifi()
        wifi.connect_wifi(args)
        base.exit_app()
    def lanuch_browser(self):
        Command(GFX_Comm['LANCH_BROWSE']).start()
        time.sleep(2)

    def input_address(self):
        try:
            self.lanuch_browser()
            checkfile.click('text="请输入网址或搜索"')
            time.sleep(1)
        except Exception,msg:
               logger.debug("Exception: %s" % msg)
               exit(1)

    def address_1(self):
        self.input_address()
        Command(GFX_Comm['ADDRESS_1']).start()
        checkfile.click('text="进入"')
    def address_2(self):
        self.input_address()
        Command(GFX_Comm['ADDRESS_2']).start()
        checkfile.click('text="进入"')

    def address_3(self):
        self.input_address()
        Command(GFX_Comm['ADDRESS_3']).start()
        checkfile.click('text="进入"')

    def address_4(self):
        self.input_address()
        Command(GFX_Comm['ADDRESS_4']).start()
        checkfile.click('text="进入"')
        time.sleep(20)
    def start_address_4(self,count):
        i = 0
        while i < count:
            Command(GFX_Comm['START_4']).start()
            time.sleep(60)
            i+=1
            logger.info('start times is %d'%i)

    def clear_history(self):
        self.input_address()
        checkfile.click('resource-id="historyClearView"')
        time.sleep(2)
        checkfile.click('text="清除"')
        status =checkfile.check_stauts('resource-id="historyClearView"')
        if status == True:
            raise Exception('clear the history is failed')
        else:
            logger.info('clear the history is success')
        base.exit_app()
    # def add_web_package(self):
    #     checkfile.click('resource-id="toolbar.toolBarView.openTabSelectorButton"')
    #     time.sleep(1)
    #     checkfile.click('resource-id="YunOSBrowser::TabSelector:Footer:AddButton"')

    def add_web_package(self):
        checkfile.click('resource-id="pageBtn"')
        time.sleep(2)
        checkfile.click('resource-id="addBtn"')

gfx=Gfxbase()

