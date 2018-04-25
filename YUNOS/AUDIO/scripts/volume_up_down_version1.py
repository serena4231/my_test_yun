#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import BaseAPI
#from AUDIO.scripts.audiobase import Audiobase version6.0
from AUDIO.scripts.audiobase_version_1 import Audiobase #version6.1
from base.checkcrash import Check_system
import time
#SETUP
def main():
    stauts = True
    try:
        Audiobase().audio_set_up()
        ####playaudio
        BaseAPI().unlock()
        Audiobase().open_audio()
        Audiobase().check_audio()
        Audiobase().play_all()
        ##change volume
        BaseAPI().change_vloume()
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts
##check result
try:
    main_test = main()
    check=Check_system().check_test_result('page://audioplayer.yunos.com')
    time.sleep(2)
    del_audio=Audiobase().delete_audio_file()
    if main_test == True and check == True and del_audio == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE
except Exception,msg:
        logger.debug('Exception:%s'%msg)
###clear
finally:
    BaseAPI().exit_app()



