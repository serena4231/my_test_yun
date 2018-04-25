#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from camerabase import camera #version6.0
from camerabase import check_videoformat
import time
#SETUP
def main():
    try:
        base.unlock()
        base.setup()
        camera.opencamera()
        camera.check_video(20)
        check_videoformat()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)




try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
    camera.teardown()
    base.reboot()


