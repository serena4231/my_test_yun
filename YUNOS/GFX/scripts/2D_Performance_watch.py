#!/usr/bin/env python
#coding:utf-8
from base.dumbase import base
import time
from base.logger import logger
from gfxbase_version_1 import gfx #version6.1
from base.checkcrash import check_system
from VIDEO.scripts.videobase_version_1 import video
def main():
    stauts = True
    try:
        video.video_set_up('animal.mp4')
        base.unlock()
        gfx.set_up('YUNOS_Auto_Test_2G')
        gfx.address_4()
        gfx.start_address_4(3)
        ##########
        video.launch_video()
        time.sleep(1)
        video.check_push_video()
        video.play_video_assign('text="animal"')
        time.sleep(80)
        base.exit_app()

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts


try:
    main_test = main()
    check=check_system.check_test_result('page://videoplayer.yunos.com')
    del_video=video.delete_video_file()
    check_package=check_system.check_test_result('page://browser.yunos.com')
    if main_test == True and check_package == True and del_video == True and check == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE

except Exception,msg:
        logger.debug('Exception:%s'%msg)

##clear
finally:
    base.exit_app()
