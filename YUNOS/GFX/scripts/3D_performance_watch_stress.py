#!/usr/bin/env python
#coding:utf-8
from base.dumbase import base
import time
from base.logger import logger
from base.checkcrash import check_system
from VIDEO.scripts.videobase_version_1 import video
from gfxbase_version_1 import gfx
def main():
    stauts = True
    try:
        video.video_set_up('animal.mp4')
        base.unlock()
        gfx.set_up('YUNOS_Auto_Test_2G')
        gfx.address_1()
        time.sleep(1)
        gfx.add_web_package()
        gfx.address_2()

        #play video with 3d high rate video

        video.launch_video()
        time.sleep(1)
        video.check_push_video()
        video.play_video_assign('text="animal"')
        video.cyclic_video()
        finished_time=video.runTask(day=1)
        if finished_time == True:
            base.exit_app()
            gfx.clear_history()
            check=check_system.check_test_result('page://videoplayer.yunos.com')
            del_video=video.delete_video_file()
            check_package=check_system.check_test_result('page://browser.yunos.com')
            if check_package == True and del_video == True and check == True:
                stauts = True
            else:
                stauts = False

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts



main_test = main()
if main_test == True:
    VERDICT = SUCCESS
else:
    VERDICT = FAILURE
