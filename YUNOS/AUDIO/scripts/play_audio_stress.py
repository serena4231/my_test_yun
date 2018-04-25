from base.logger import logger
from base.dumbase import base
#from AUDIO.scripts.audiobase import Audiobase version6.0
from AUDIO.scripts.audiobase_version_1 import Audiobase
from base.checkcrash import Check_system
import time
from VIDEO.scripts.videobase_version_1 import video
#SETUP
def main():
    stauts = True
    try:
        Audiobase().audio_set_up()
        ####playaudio
        base.unlock()
        Audiobase().open_audio()
        Audiobase().check_audio()
        Audiobase().play_all()
        finish_time=video.run_Task()
        if finish_time == True:
            Check_system().check_test_result('page://audioplayer.yunos.com')
            time.sleep(2)

    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts
##check result
try:
    main_test = main()
    del_audio=Audiobase().delete_audio_file()
    if main_test == True and del_audio == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE
except Exception,msg:
        logger.debug('Exception:%s'%msg)
###clear
finally:
    base.exit_app()


