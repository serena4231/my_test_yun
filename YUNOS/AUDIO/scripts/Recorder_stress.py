from base.logger import logger
from base.dumbase import BaseAPI
#from AUDIO.scripts.audiobase import Recorbase  #version6.0
from AUDIO.scripts.audiobase_version_1 import Recorbase #version6.1
from base.checkcrash import Check_system
import time
def main():
    stauts = True
    try:
        ########set up
        BaseAPI().unlock()
        BaseAPI().setup()
        ###recorder sounds
        i=0
        while i < 30:
            Recorbase().launch_recor_package()
            Recorbase().recorder_cycle(20)
            i+=1
            logger.info("Recorder is try: %d" %(i))
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts



##check result
try:
    main_test = main()
    check=Check_system().check_test_result('page://recorder.yunos.com')
    time.sleep(2)
    del_recor=Recorbase().delete_recorder()
    if main_test == True and check == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE
except Exception,msg:
        logger.debug('Exception:%s'%msg)

##clear
finally:
    BaseAPI().exit_app()



