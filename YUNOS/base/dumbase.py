#!usr/bin/env python
#coding:utf-8
from logger import logger
from baseflash import Command
import os
import re
import shutil
import time
from baseflash import check_adb_device
import random

cur_dir = os.getcwd()

log_path = os.path.join(cur_dir,'dumplog')
Comm = {
    'SCREEN_ON':'adb -host shell input keyevent 26',
    'UNLOCK':'adb -host shell input swipe 632 632 1280 766',
    'C_DUMP':'adb -host shell uiautomator',
    'P_DUMP':'adb -host pull /var/log/uidump.txt ',
    'HOME':'adb -host shell input keyevent 3',
    'BACK':'adb -host shell input keyevent 4',
    'DELETE':'adb -host shell input keyevent --longpress 67',
    'SWIPE_SETTING':'adb -host shell input swipe 99 642 92 121',
    'OPENSETTING':'adb -host shell sendlink "page://settings.yunos.com/settings"',
    'SYSTEM_STTING':'adb -host shell input tap 98 645',
    'RECOVERY_SYSTEM':'adb -host shell input tap 49 78',
    'RECOVER':'adb -host shell input tap 445 682',
    'FINISH_RECOVER':'adb -host shell input tap 511 688',
    'DISPLAY':'adb -host shell input tap 93 365',
    'LOCK_DISPLAY':'adb -host shell input tap 49 258',
    'DISPLAY_NEVER':'adb -host shell input tap 82 580',
    'REBOOT':'adb -host reboot',
    'START_SETTING':'adb -host shell input tap 500 742',
    'CHOOSE_UNINSTALL_RECOVERY':'adb -host shell input tap 100 214',
    'CHOOSE_FORMAT_RECOVERY':'adb -host shell input tap 100 260',
    'VOLUME':'adb -host shell input tap 100 445',
    'VOLUME_UP':'adb -host shell input tap 800 200',
    'VOLUME_DOWN':'adb -host shell input tap 100 200',
    'VOLUME_UP_TO_DOWN':'adb -host shell input swipe 800 200 100 200',
    'VOLUME_DOWN_TO_UP':'adb -host shell input swipe 100 200 800 200',
    'KEY_VOLUME_LONG_UP':'adb -host shell input keyevent --longpress 24',
    'KEY_VOLUME_LONG_DOWN':'adb -host shell input keyevent --longpress 25',
    'KEY_VOLUME_MUTE':'adb -host shell input keyevent 91'
}

class Checkfile():

    def create_dump(self):
        return Command(Comm['C_DUMP']).start()
        time.sleep(1)

    def position(self,args):
        self.create_dump()
        states,f,error=Command('adb -host shell cat /var/log/uidump.txt').start()
        for line in f.splitlines():
            serach = re.compile(args)
            d= serach.findall(line)
            if d ==[]:
                pass
            else:
                spl = line.strip()
                # rtn =re.search(r'(\d+)\,(\d+)\]\[(\d+)\,(\d+)',spl).groups()
                rtn = re.search(r'(\d+[.\d]*)\,(\d+[.\d]*)\]\[(\d+[.\d]*)\,(\d+[.\d]*)',spl)
                rtn_x1=int(rtn.group(1).split('.')[0])
                rtn_y1=int(rtn.group(2).split('.')[0])
                rtn_x2=int(rtn.group(3).split('.')[0])
                rtn_y2=int(rtn.group(4).split('.')[0])
                x = random.randint(rtn_x1,rtn_x2)
                print(x)
                y = random.randint(rtn_y1,rtn_y2)
                print(y)
                return x,y

    def click(self,args):
        x,y=self.position(args)
        time.sleep(1)
        status,output,error=Command('adb -host shell input tap {0} {1}'.format(x,y)).start()
        base.check_adb_command('ret = true',output)
    def long_click(self,args):
        x,y=self.position(args)
        time.sleep(1)
        status,output,error=Command('adb -host shell input longtap {0} {1}'.format(x,y)).start()
        base.check_adb_command('ret = true',output)
    #########################################################

    def get_new_logfile(self):
        new_logfile = os.listdir(log_path)
        new_logfile.sort(key=lambda fn: os.path.getmtime(log_path+fn) if not os.path.isdir(log_path+fn) else 0)
        return new_logfile[-1]



    def check_stauts(self,*args):
        self.create_dump()
        states,out,error=Command('adb -host shell cat /var/log/uidump.txt').start()
        status = True
        for i in args:
            search = re.compile(i)
            d=search.findall(out)
            if d ==[]:
                logger.debug('cannot find matched content:%s'%i)
                status=False
            else:
                logger.info('keyword matched in file:%s'%i)
        return status


class Checkpath():

    def create_newlog_path(self,path=log_path):
        os.makedirs(path)
        return os.path.exists(path)

    def remove_newlog_path(self,path = log_path):
        try:
            shutil.rmtree(path)
        except:
            logger.debug('Can not remove the directory')



class BaseAPI():
    def setup(self):
        # Checkpath().create_newlog_path()
        # logger.info('create the dump log')
        Command(Comm['OPENSETTING']).start()
        time.sleep(2)
        # Command(Comm['DISPLAY']).start()
        checkfile.click('显示')
        time.sleep(2)
        checkfile.click('锁屏休眠')
        time.sleep(1)
        checkfile.click('永不')
        # Command(Comm['LOCK_DISPLAY']).start()
        # Command(Comm['DISPLAY_NEVER']).start()
        status=checkfile.check_stauts('text="永不"')
        if status == True:
            logger.info('opened the display never lock')
            self.exit_app()
        else:
            logger.debug('cannot open the display never lock')
            exit(1)


    def teardown(self):
        Checkpath().remove_newlog_path()
        logger.info('rmove the dump log ')

    def screen_on(self):
        try:
            Command(Comm['SCREEN_ON']).start()
            logger.info('screen_on_off_screen')
            return True
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            return False
    def unlock(self):
        check_adb_device()
        Command(Comm['UNLOCK']).start()
        logger.info('unlock the screen is successed')
        time.sleep(2)
    def home(self):
        Command(Comm['HOME']).start()
        status=checkfile.check_stauts('text="应用中心"')

        if status == True:
            logger.info('return to home is successed')
        else:
            raise Exception('return to home is failed')

    def back(self):

        Command(Comm['BACK']).start()
        logger.info('back to next')



    def recover_system(self):
        Command(Comm['OPENSETTING']).start()
        checkfile.check_stauts('text="云服务"')
        Command(Comm['SWIPE_SETTING']).start()
        Command(Comm['SYSTEM_STTING']).start()
        Command(Comm['RECOVERY_SYSTEM']).start()
        checkfile.check_stauts('text="格式化内部存储"')
        #choose unistall app and format store

        Command(Comm['CHOOSE_UNINSTALL_RECOVERY']).start()
        Command(Comm['CHOOSE_FORMAT_RECOVERY']).start()
        #确认恢复出厂设置
        Command(Comm['RECOVER']).start()
        Command(Comm['FINISH_RECOVER']).start()

    def recover_system_new(self):
        Command(Comm['OPENSETTING']).start()
        checkfile.check_stauts('text="云服务"')
        Command(Comm['SWIPE_SETTING']).start()
        Command(Comm['SYSTEM_STTING']).start()
        Command('adb -host shell input tap 140 200').start()
        #choose unistall app and format store
        Command(Comm['CHOOSE_UNINSTALL_RECOVERY']).start()
        Command(Comm['CHOOSE_FORMAT_RECOVERY']).start()
        #确认恢复出厂设置
        Command(Comm['RECOVER']).start()
        Command(Comm['FINISH_RECOVER']).start()


    def reboot(self):
        Command(Comm['REBOOT']).start()
        time.sleep(60)
        check_adb_device()
        status =checkfile.check_stauts('text="滑动解锁"')
        if status == True:
            logger.info('Reboot DUT is Success')
        else:
            raise Exception('Reboot DUT is Failed')
    def reboot_version1(self):
        Command(Comm['REBOOT']).start()
        time.sleep(230)
        check_adb_device()
        time.sleep(3)
        base.screen_on()
        time.sleep(2)

    def find_setting(self):
        Command(Comm['OPENSETTING']).start()
        time.sleep(2)
        status =checkfile.check_stauts('text="蓝牙"')
        if status == True:
            logger.info('open setting is successed')
        else:
            raise Exception('open setting is failed')

    def setting_reboot(self):
        try:
            self.reboot()
            self.unlock()
            self.find_setting()
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)
    def setting_reboot_version1(self):
        try:
            self.reboot_version1()
            self.unlock()
            self.find_setting()
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)
    def setting_afterflash(self):
        try:
            i =0
            while i < 5:
                Command(Comm['START_SETTING']).start()
                i+=1
                time.sleep(1)
            logger.info('finished the setting')

        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)


    def exit_app(self):
        try:
            i = 0
            while i < 5:
                Command(Comm['BACK']).start()
                i+=1
            logger.info('back to home and exit app')
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)


    def longpress_delete(self):
        Command(Comm['DELETE']).start()

    def vloume_change_up_down(self):
        self.find_setting()
        Command(Comm['VOLUME']).start()
        volume_states = checkfile.check_stauts('text="静音"')
        if volume_states == True:
            logger.info('open volume is success')

        else:
            logger.debug('open volume is failed')
            exit(1)
        Command(Comm['VOLUME_DOWN']).start()
        Command(Comm['VOLUME_UP_TO_DOWN']).start()
        time.sleep(5)
        Command(Comm['VOLUME_DOWN_TO_UP']).start()
        time.sleep(5)

    def change_vloume(self):
        Command('adb -host shell input keyevent --longpress 24').start()
        time.sleep(5)
        Command('adb -host shell input keyevent --longpress 25').start()
    def up_down(self):
        Command(Comm['VOLUME_DOWN']).start()
        Command(Comm['VOLUME_UP_TO_DOWN']).start()
        time.sleep(5)
        Command(Comm['VOLUME_DOWN_TO_UP']).start()
        time.sleep(5)

    def mute_sound(self):
        result = r'ret = true'
        states,output,error =Command(Comm['KEY_VOLUME_MUTE']).start()
        output = output.rstrip().rsplit(',')
        if not result == output[1]:
            raise Exception('mute the sound is failed')
        logger.info('mute the sound is success')
        time.sleep(1)
    def long_press_vloumeup(self):
        result = r'ret = true'
        tates,output,error =Command(Comm['KEY_VOLUME_LONG_UP']).start()
        output = output.rstrip().rsplit(',')
        if not result == output[1]:
            raise Exception('long press volume up is failed')
        logger.info('ong press volume up is success')
        time.sleep(1)



    def check_adb_command(self,args,output):
        serach = re.compile(args)
        d = serach.findall(output)
        if d ==[]:
            raise Exception('adb command operation failed')
    def change_unmute_mute(self,count):
        i = 0
        while i <count:
            BaseAPI().mute_sound()
            time.sleep(1)
            BaseAPI().long_press_vloumeup()
            logger.info("mute and umute the sound try: %d" %(i))
            i+=1


class Checkfile_local():
    def __init__(self,filename):
        self.filename = filename

    def pull_file(self):
        timestamp= time.strftime("%Y-%m-%d-%H-%M-%S")
        creat_logname=os.path.join(log_path,'{1}_dump_{0}.log'.format(timestamp,self.filename))
        time.sleep(1)
        Command(Comm['P_DUMP']+ creat_logname).start()
        print(creat_logname)
        return creat_logname


    def readContent(self):
        f = open(self.pull_file(),'rb')
        content = f.read()
        return content
    def check_devices_location(self,*args):
        Checkfile().create_dump()
        status = True
        content = self.readContent()
        for i in args:
            serach = re.compile(i)
            d= serach.findall(content)
            if d ==[]:
                logger.debug('cannot find matched content : %s' % i)
                status = False
            else:
                logger.info('keyword matched in file :%s' % i)

        return status
base=BaseAPI()
checkfile = Checkfile()
checkpath = Checkpath()
