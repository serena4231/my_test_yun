#!/usr/bin/env python
#coding:utf-8

from base.baseflash import Command
from base.logger import logger
from base.dumbase import checkfile
from base.dumbase import Checkpath
from base.dumbase import BaseAPI
import time
import re

path_local ='/home/buildbot/audiofile'
path_devcices ='/storage/emulated/0/' ###version6.1path
Audio_Comm={
    'OPENAUDIO':'adb shell sendlink "page://musicplayer.yunos.com/musicplayer"',
    'PUSHAUDIO':'adb push {0} {1}'.format(path_local,path_devcices),
    'PLAY_ALL':'adb shell input tap 100 100',
    'PLAY_BUTTON':'adb shell input tap 660 680',
    'PROPERTY_MISC':'adb shell input tap 1200 150',
    'SEEK_MID':'adb shell input tap 662 650',
    'SEEK_START':'adb shell input tap 5 650',
    'SEEK_END':'adb shell input tap 1100 650',
    'DELETE_CHOICE':'adb shell input tap 1200 108',
    'DELETE_CLICK':'adb shell input tap 1240 30',
    'DELETE_AUDIO':'adb shell input tap 770 700',
    'CONFIRM_DELETE':'adb shell input tap 700 440',
    'VOLUME_SETTING':'adb shell input tap 100 440',

}


class Audiobase():

    def open_audio(self):
        Command(Audio_Comm['OPENAUDIO']).start()

        status =checkfile.check_stauts('text="未知艺人"')
        if status == True:
            logger.info('SUCCESS:open audio package is success')
        else:
            logger.debug('Failed:open audio package is failed')
            exit(1)
    def push_audiofile(self):
        try:
            Command(Audio_Comm['PUSHAUDIO']).start()
            logger.info('push audio file in devices')
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)
    def check_audio(self):
        time.sleep(2)
        status = checkfile.check_stauts('text="无音乐"')

        if status == False:
            logger.info('SUCCESS:push audio file is success')
        else:
            logger.debug('Fail:push audio file is failed')
            exit(1)
    def play_all(self):
        Command(Audio_Comm['PLAY_ALL']).start()
        time.sleep(3)
        status = checkfile.check_stauts('text="00:03/01:00"')
        if status == True:
            logger.info('Play audio is success')
        else:
            logger.error('Play audio is failed')

    def play_button(self):
        if not Command(Audio_Comm['PLAY_BUTTON']).start():
            raise Exception("Click the audio play button is not success ")

    def check_pause(self,timeout = 10):
        time.sleep(timeout)
        self.play_button()
        time.sleep(2)
        if not checkfile.check_stauts('text="00:14/01:00"'):
             raise Exception("Pause the audio play is faied")



    def seek__player_start(self):
        Command(Audio_Comm['SEEK_START']).start()

    def seek_player_mid(self):
        Command(Audio_Comm['SEEK_MID']).start()

    def seek_player_end(self):
        Command(Audio_Comm['SEEK_END']).start()


    def seek_player(self):
        try:
            self.seek__player_start()
            self.seek_player_end()
            self.seek_player_mid()
        except Exception,msg:
            logger.debug('FAILED:%s'%msg)
            exit(1)
    def pause_resume_player(self):
        try:
             self.play_all()
             self.check_pause()
             self.play_button()
        except Exception,msg:
            logger.debug('FAILED:%s'%msg)
            exit(1)
    def delete_audio_file(self):
        checkfile.click('管理')
        time.sleep(2)
        Command(Audio_Comm['DELETE_CLICK']).start()
        time.sleep(2)
        Command(Audio_Comm['DELETE_AUDIO']).start()
        time.sleep(1)
        Command('adb -host shell input tap 700 450').start()
        time.sleep(2)
        BaseAPI().back()
        status = checkfile.check_stauts('text="暂无音乐"')
        time.sleep(2)
        if status == True:
            logger.info('Delete the audio file is success')
            return True
        else:
            logger.debug('Delete the audio file is failed')
            return False


    def volume_up(self):
        BaseAPI().find_setting()
        Command(Audio_Comm['VOLUME_SETTING']).start()
        status = checkfile.check_stauts('text="静音"')
        if not status == True:
            raise Exception('open the volume  is failed')

    def audio_set_up(self):
        BaseAPI().unlock()
        BaseAPI().setup()
        Audiobase().push_audiofile()
        logger.info('setup audio test')


Recorder_Comm={'OPEN_RECORDER':'adb -host shell sendlink page://recorder.yunos.com/recorder',
               'START_RECORDER':'adb -host shell input tap 620 700',
               'SAVE_RECORDER':'adb -host shell input tap 700 400',
               'RECORDER_LIST':'adb -host shell input tap 1240 30',
               'PLAY_RECODER':'adb -host shell input tap 300 100',
               'CHOICE_LIST':'adb -host shell input tap 1240 30',
               'DELETE':'adb -host shell input tap 650 700',
               'CONFRIM_DELETE':'adb -host shell input tap 700 430',}
class Recorbase():
    def launch_recor_package(self):
        status,output,error=Command(Recorder_Comm['OPEN_RECORDER']).start()
        BaseAPI().check_adb_command('SUCCESS',output)

    def start_stop_recorder(self):
        status,output,error=Command(Recorder_Comm['START_RECORDER']).start()
        BaseAPI().check_adb_command('ret = true',output)
    def save_recorder(self):
        status,output,error=Command(Recorder_Comm['SAVE_RECORDER']).start()
        BaseAPI().check_adb_command('ret = true',output)


    def play_recorder(self,count):
        Command(Recorder_Comm['RECORDER_LIST']).start()
        status,output,error=Command(Recorder_Comm['PLAY_RECODER']).start()
        BaseAPI().check_adb_command('ret = true',output)
        time.sleep(count)

    def delete_recorder(self):
        self.launch_recor_package()
        status = checkfile.check_stauts('text="录音列表"')
        if status == False:
            count = 3
        else:
            count =2
        for i in range(count):
            Command(Recorder_Comm['RECORDER_LIST']).start()

        Command(Recorder_Comm['DELETE']).start()
        checkfile.click('text="确定"')
    def recorder_cycle(self,count):
        i = 0
        while i<2:
            self.start_stop_recorder()
            time.sleep(count)
            i+=1
            count = 0
        time.sleep(1)
        self.save_recorder()
        time.sleep(1)
        self.play_recorder(2)
        time.sleep(1)
        BaseAPI().back()
