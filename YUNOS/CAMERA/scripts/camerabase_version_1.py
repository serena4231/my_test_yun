#!/usr/bin/env python
#coding:utf-8

from base.baseflash import Command
from base.logger import logger
import time
from base.dumbase import Checkpath
from base.dumbase import checkfile
from base.dumbase import BaseAPI
from PIL import Image
import os
import cv2

cur_dir = os.getcwd()
camera_path = os.path.join(cur_dir,'Camera')
Camera_Comm={
    'OPENCAMERA':'adb -host shell sendlink page://camera.yunos.com/camera',
    'CLICK': 'adb -host shell input tap 623 700',
    'SWTICH_STATUS':'adb -host shell input tap 514 700',
    'CAMERA_FILE':'adb -host shell input tap 22 682',
    'CAMERA_SETTING':'adb -host shell input tap 1239 700',
    'RECORD_PAUSE':'adb -host shell input tap 1239 700',
    'CREATE_CAMERA':'adb -host pull /mnt/data/yunos/share/media/0/DCIM/Camera ',
    'REMOVE_VIDEO':'adb -host shell rm -r /mnt/data/yunos/share/media/0/DCIM/Camera',

}


class Camerabase():
    def opencamera(self):
        Command(Camera_Comm['OPENCAMERA']).start()
        # status=checkfile.check_stauts('object="page://camera.yunos.com/camera"')
        # if status == True:
        #     logger.info('opencamera is successed')
        # else:
        #     logger.debug('opencamera is failed')
        #     exit(0)

    def camera_button(self):
        check_status=Command(Camera_Comm['CLICK']).start()
        logger.info(check_status)
        time.sleep(1)
        Command(Camera_Comm['CAMERA_FILE']).start()
        time.sleep(2)
        status=checkfile.check_stauts('page://gallery.yunos.com/Gallery')
        if status == True:
            logger.debug('take picture is successed')
        else:
            raise Exception('take picture is failed')


    def video_button(self,seconds):
        time.sleep(1)
        Command(Camera_Comm['SWTICH_STATUS']).start()
        time.sleep(1)
        logger.info('switch to  video mode')
        i = 0
        while i<2:
           try:
                time.sleep(2)
                Command(Camera_Comm['CLICK']).start()
                logger.info('click the video button')
                time.sleep(seconds)
                i+=1
                seconds = 0
           except Exception,msg:
               logger.debug("Exception: %s" % msg)
               exit(1)

    def check_video(self,seconds):
        try:
            self.video_button(seconds)
            time.sleep(3)
            Command(Camera_Comm['CAMERA_FILE']).start()
            time.sleep(3)
            status=checkfile.check_stauts('"page://videoplayer.yunos.com/videoplayer"')
            if status == True:
                logger.info('play video is successed')

            else:
                logger.debug('play video is failed')
                exit(0)

        except Exception, msg:
            logger.debug("Exception: %s" % msg)


    # def camera_setting(self):
    #     # Command(Camera_Comm['CAMERA_SETTING']).start()
    #     status=check_stauts('camerasetting','text="相机声音"')
    #     if status == True:
    #         logger.info('open camera setting is successed')
    #         check_stauts('camera_volume','checked=')
    #
    #     else:
    #         logger.debug('open camera setting is failed')

    def teardown(self):
        Command(Camera_Comm['REMOVE_VIDEO']).start()
        Checkpath().remove_newlog_path(path= camera_path)
        logger.info('remove the camera_video file is success')
        time.sleep(1)

    def check_camera_size(self):
        time.sleep(1)
        Checkpath().create_newlog_path(path= camera_path)
        Command(Camera_Comm['CREATE_CAMERA']+camera_path).start()
        s = os.listdir(camera_path)
        for i in s:
            image_pic = Image.open(camera_path+'/'+i)
            image=image_pic.size
            if image[1]!= 720:
                raise Exception('The picture is not 720P:FAILED')
            else:
                logger.info('The picture is 720P:SUCCESS')
    def check_video_size(self):
        Checkpath().create_newlog_path(path= camera_path)
        Command(Camera_Comm['CREATE_CAMERA']+camera_path).start()
        s = os.listdir(camera_path)
        for i in s:
            video = cv2.VideoCapture(camera_path+'/'+i)
            # cv2.CAP_PROP_FRAME_HEIGHT  for windows
            # cv2.CAP_PROP_FRAME_WIDTH
            size = (int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
            if size[1]!= 720:
                raise Exception('The video is not 720P:FAILED')
            else:
                logger.info('The video is 720P:SUCCESS')

def endWith(s,*endstring):
    array = map(s.endswith,endstring)
    if True in array:
            return True
    else:
            return False




def check_videoformat():
    Checkpath().create_newlog_path(path= camera_path)
    Command(Camera_Comm['CREATE_CAMERA']+camera_path).start()
    time.sleep(5)
    try:
        s = os.listdir(camera_path)
        for i in s:
            if endWith(i,'.mp4'):
                logger.info(i)
                logger.info('The type is matched')
            else:
                logger.debug('The type is failed')
                exit(1)
    except Exception,msg:
        logger.debug('Exception:%s'%msg)


camera = Camerabase()