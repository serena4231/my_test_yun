#!/usr/bin/env python
#coding:utf-8
from base.baseflash import Command
from base.logger import logger
import time
from base.dumbase import checkfile
from base.dumbase import BaseAPI
import os
from datetime import date, datetime, timedelta
#path_devcices ='/run/mount/emulated'  ###version6.0path
path_devcices ='/storage/emulated/0/' ###version6.1path
path_local=r'/home/buildbot/videofile/'

Video_Comm={
    'OPENVIDEO':'adb -host shell sendlink page://videoplayer.yunos.com/videoplayer',
    'PLAYVIDEO':'adb -host shell input tap 200 200',
    'MORE':'adb -host shell input tap 1250 35',
    'EDITOR':'adb -host shell input tap 1200 255',
    'CHOICCE':'adb -host shell input tap 1240 30',
    'DELETE_OPTION':'adb -host shell input tap 720 730',
    'CONFRIM_DELETE':'adb -host shell input tap 700 450',
    'CLICK_SCREEN':'adb -host shell input tap 300 700',
    'SEEK_START_LOCAL':'adb -host shell input swipe 100 700 900 700',
    'SEEK_RETURN_LOCAL':'adb -host shell input swipe 1000 700 100 700',
    'PAUSE_RESUME':'adb -host shell input keyevent 62',
    'SEEK_LEFT_KEYEVENT':'adb -host shell input keyevent 21',
    'SEEK_RIGHT_KEYEVENT':'adb -host shell input keyevent 22',


}

class videobase():
    def launch_video(self):
        Command(Video_Comm['OPENVIDEO']).start()
        time.sleep(2)
        status=checkfile.check_stauts('page://videoplayer.yunos.com/videoplayer')
        if status == True:
            logger.info('open the video app is success')
        else:
            raise Exception("Launch video player is failed")

    def push_video_file(self,*args):
        try:
            for i in args:
                Command('adb -host push {0} {1}'.format(os.path.join(path_local,i),path_devcices)).start()
                time.sleep(5)
                logger.info('push video file in devices')
        except Exception,msg:
            logger.debug('Exception:%s'%msg)
            exit(1)


    def check_push_video(self):
        time.sleep(3)
        status = checkfile.check_stauts('text="暂无视频"')
        if status == False:
            logger.info('SUCCESS:push video file is success')
        else:
            raise Exception('Fail:push video file is failed')


    def play_video(self):
        Command(Video_Comm['PLAYVIDEO']).start()
        status =checkfile.check_stauts('resource-id="playerView"')
        if status == True:
            logger.info('play video is success')
        else:
            raise Exception('play video is failed')

    def play_video_assign(self,args):
        checkfile.click(args)
        time.sleep(5)
        status =checkfile.check_stauts('resource-id="playerView"')
        if status == True:
            logger.info('play video is success')
        else:
            raise Exception('play video is failed')
    def delete_video_file(self):
        self.launch_video()
        Command(Video_Comm['MORE']).start()
        time.sleep(1)
        Command(Video_Comm['EDITOR']).start()
        Command(Video_Comm['CHOICCE']).start()
        time.sleep(1)
        Command(Video_Comm['DELETE_OPTION']).start()
        Command(Video_Comm['CONFRIM_DELETE']).start()
        status = checkfile.check_stauts('text="暂无视频"')
        if status == True:
            logger.info('Delete the video file is  success')
            return True
        else:
            logger.debug('Delete the video file is  failed')
            return False

    def check_video_afterunlock(self):
        status =checkfile.check_stauts('text=00:23')
        if status == True:
            raise Exception('play video after unlock screen is failed')
        else:
            logger.info('play video after unlock screen is success')
    def video_set_up(self,*args):
        status= True
        try:
            BaseAPI().unlock()
            BaseAPI().setup()
            videobase().push_video_file(*args)
            BaseAPI().reboot()
        except Exception,msg:
            logger.debug('FAILED:%s'%msg)
            status = False
            exit(1)
        return status


    def seek_video(self,count):
        i = 0
        while i < count:
            Command(Video_Comm['SEEK_START_LOCAL']).start()
            status,output,error=Command(Video_Comm['SEEK_RETURN_LOCAL']).start()
            BaseAPI().check_adb_command('ret = true',output)
            i+=1
            logger.info("seek the video try: %d" %(i))

    def pause_resume(self,count):
        i = 0
        while i < count:
            status,output,error=Command(Video_Comm['PAUSE_RESUME']).start()
            BaseAPI().check_adb_command('ret = true',output)
            time.sleep(1)
            i+=1
            logger.info('pause and play video try: %d' %(i))
    def cyclic_video(self):
        time.sleep(5)
        #click screen
        Command('adb -host shell input tap 500 600').start()
        Command('adb -host shell input tap 1240 30').start()
        Command('adb -host shell input tap 1240 100').start()
    def runTask(self,day=0, hour=0, min=0, second=0):
        finished_time = False
       # Init time
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        print "now:",strnow
       #stop time
        period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
        next_time = now + period
        strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
        print "stop time:",strnext_time
        # video.play_video()
        while True:
               # Get system current time
            iter_now= datetime.now()
            iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
            if str(iter_now_time) == str(strnext_time):
                logger.info('task done')
                break
        return finished_time

video = videobase()
