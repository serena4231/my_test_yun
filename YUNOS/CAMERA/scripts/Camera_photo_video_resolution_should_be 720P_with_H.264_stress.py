#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from camerabase import camera #version6.0
import time
from base.dumbase import Command
#SETUP
def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        camera.opencamera()
        camera.camera_button()
        time.sleep(1)
        # camera.check_camera_size()
        camera.teardown()
        base.exit_app()
        ###########take one minute video
        camera.opencamera()
        camera.video_button(90)
        i = 0
        while i <30:
            Command('adb -host shell input tap 623 700').start()
            logger.info('click the video button')
            time.sleep(60)
            Command('adb -host shell input tap 623 700').start()
            time.sleep(1)
            i+=1

        camera.check_video_size()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)
        stauts = False

    finally:
        camera.teardown()
        base.reboot()

    return stauts

main= main()
if main == True:
    VERDICT = SUCCESS
else:
     VERDICT = FAILURE

