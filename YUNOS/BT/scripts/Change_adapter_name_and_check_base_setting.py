#!/usr/bin/env python
#coding:utf-8
from base.logger import logger
from base.dumbase import base
from btbase import bt
import time

def main():
#SETUP
    try:
        base.unlock()
        base.setup()

#Change the adapter name.
        base.find_setting()
        bt.enable_bt()
        bt.change_adapter_name('YUNOS')
        base.back()
        bt.disable_bt()

        ###########disable and enable bt
        base.back()
        bt.enable_bt()
        bt.check_adapter_name('text="YUNOS"')

        #########################
        bt.start_scanner()
        bt.stop_scanner()
        bt.check_adapter_name('text="YUNOS"')
        time.sleep(1)
        bt.revert_adapter_name()


    except Exception,msg:
        logger.debug('Exception:%s'%msg)



try:
    main()
    VERDICT = SUCCESS
except Exception as msg:
     VERDICT = FAILURE
finally:
     base.exit_app()
