#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
#from videobase import video #version6.0
from videobase_version_1 import video #versin6.1
from base.checkcrash import Check_system
import time



def main():
    stauts = True
    try:
        ########setup
        video.video_set_up('dayu.mp4')
        #####play video
        base.unlock()
        time.sleep(3)
        video.launch_video()
        time.sleep(1)
        video.check_push_video()
        video.play_video()
        time.sleep(5)
        video.cyclic_video()
        i = 0
        while i <100:
            time.sleep(1)
            base.screen_on()
            time.sleep(1)
            base.screen_on()
            base.unlock()
            i+=1
            logger.info('poweroff_screen try: %d' %(i))
        ##########
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    finally:
        base.exit_app()
    return stauts
try:
    main_test = main()
    check=Check_system().check_test_result('page://videoplayer.yunos.com')
    del_video=video.delete_video_file()
    if main_test == True and check == True and del_video == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE
except Exception,msg:
        logger.debug('Exception:%s'%msg)
###clear
finally:
    base.exit_app()

