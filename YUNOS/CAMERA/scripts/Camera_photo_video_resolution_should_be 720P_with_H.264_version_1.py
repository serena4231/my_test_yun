#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from camerabase_version_1 import camera
#from camerabase import camera #version6.0
import time

#SETUP
def main():
    stauts = True
    try:
        base.unlock()
        base.setup()
        camera.opencamera()
        camera.camera_button()
        time.sleep(1)
        camera.check_camera_size()
        time.sleep(2)
        camera.teardown()
        base.exit_app()
        ###########take one minute video
        camera.opencamera()
        camera.video_button(60)
        # camera.check_video_size()
    except Exception,msg:
        logger.debug('FAILED:%s'%msg)
        stauts = False

    finally:
        camera.teardown()
        base.reboot_version1()
        base.unlock()

    return stauts

main= main()
if main == True:
    VERDICT = SUCCESS
else:
     VERDICT = FAILURE

