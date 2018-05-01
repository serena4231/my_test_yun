#!/usr/bin/env python
#coding:utf-8

from base.logger import logger
from base.dumbase import base
#from AUDIO.scripts.audiobase import Audiobase version6.0
from AUDIO.scripts.audiobase_version_1 import Audiobase #version6.1
#SETUP

def play_audio_pause_seek():
    status =True
    try:
        Audiobase().open_audio()
        Audiobase().check_audio()
        base.reboot()
        Audiobase().pause_resume_player()
        Audiobase().seek_player()

    except Exception,msg:
        logger.debug('FAILED:%s'%msg)
        status = False
    return status

def main():

    Audiobase().audio_set_up()
    ####playaudio
    base.unlock()
    status = play_audio_pause_seek()
    if status == True:
        logger.info('play mp3 is succes')
    else:
        logger.debug('play mp3 is failed')


try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
    logger.debug('FAILED:%s'%msg)
    VERDICT = FAILURE
finally:
     Audiobase().delete_audio_file()
     base.exit_app()


