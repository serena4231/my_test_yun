from base.dumbase import base
from base.logger import logger
from gfxbase_version_1 import gfx
from base.checkcrash import check_system
def main():
    stauts = True
    try:
        gfx.set_up('YUNOS_Auto_Test_2G')
        gfx.address_3()
    except Exception,msg:
        logger.debug('Exception:%s'%msg)
        stauts = False
    return stauts


try:
    main_test = main()
    check_package=check_system.check_test_result('page://browser.yunos.com')
    if main_test == True and check_package == True:
        VERDICT = SUCCESS
    else:
        VERDICT = FAILURE

except Exception,msg:
        logger.debug('Exception:%s'%msg)

###clear
finally:
    base.exit_app()
