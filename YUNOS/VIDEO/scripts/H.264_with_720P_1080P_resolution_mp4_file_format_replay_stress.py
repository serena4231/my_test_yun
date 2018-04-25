#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
# from videobase import video #version6.0
from videobase_version_1 import video #versin6.1
from base.checkcrash import check_system
import time



def main():
    stauts = True
    try:
        video.video_set_up('animal.mp4')
        base.unlock()
        time.sleep(3)
        video.launch_video()
        time.sleep(1)
        video.check_push_video()
        video.play_video()
        time.sleep(10)
        video.cyclic_video()
        finish_time=video.run_Task()
        if finish_time == True:
            check_system.check_test_result('page://videoplayer.yunos.com')
            base.exit_app()
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts


main_test = main()
if main_test == True:
    video.delete_video_file()
    base.exit_app()
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE


