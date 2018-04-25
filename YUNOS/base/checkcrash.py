import time
import subprocess

from baseflash import Command
from logger import logger


class Check_system():
    def checkforpanic(self):

         """
         Check for panic files at /mnt/data/yunos/var/tools/apr/log/panic
         """

         panic_file = subprocess.check_output( 'adb -host shell \"ls /mnt/data/yunos/var/tools/apr/log/panic\"',shell=True)
         print(panic_file)
         if len(panic_file) > 0:
            logger.info("PANIC Files found!!!")
            return 0
         else :
            logger.info(" No PANIC Files found!!!")
            return 1

    def checkfortombstones(self):

         """
         Check for tombstones files at mnt/data/yunos/var/tools/apr/log/c_tombstone
         """

         tombstone_file = subprocess.check_output( 'adb -host shell \"ls /mnt/data/yunos/var/tools/apr/log/c_tombstone\" ',shell=True)
         print(tombstone_file)
         if len(tombstone_file) > 0:
            logger.info("TOMBSTONE Files found!!!")
            return 0
         else :
            logger.info("No TOMBSTONE Files found!!!")
            return 1


    # Removing all dontpanic files already present
    def remove_panic_file(self):

        logger.info("Removing already present PANIC")
        Command("adb -host shell rm -rf /mnt/data/yunos/var/tools/apr/log/panic/*").start(10)

    # Removing all tombstones already present
    def remove_tomstones(self):

        logger.info("Removing already present TOMBSTONES")
        Command("adb -host shell rm -rf /mnt/data/yunos/var/tools/apr/log/c_tombstone/*").start(10)


    #Checking for all crashes
    def check_all_crashes(self):
        if (self.checkforpanic() == 1)and (self.checkfortombstones() == 1) :
            logger.info("No crashes found :Pass")
            return True
        else :
            logger.debug("Crashes Found : FAIL")
            return False
    #checking devices status
    def check_device_status(self):
        status =False
        count =0
        logger.info("Checking device status")
        while count < 3:
            # check host-dut adb status
            ex_status,output,error = Command("adb -host get-state").start(timeout=3)
            if output.rstrip() != r"device":
                logger.info("adb device state: %s try: %d" %(output,count))
            else:
                # check if adb is working
                logger.info("adb device state: %s" % output)
                exec_status, output,error = Command("adb -host shell getprop ro.yunos.build.id").start()
                output=output.rstrip()
                if len(output) > 0:
                    logger.info("Output of 'adb shell getprop ro.yunos.build.id' is (%s)" % output)
                    status=True
                    break
            count += 1
        return status


    ####check_package still alive
    def check_package_status(self,package):
        status = False
        output = Command('adb -host shell \"ps -ef| grep %s"'%package).start()
        if len(output)> 0:
           logger.info('package is still alive')
           status = True
        return status
    def check_test_result(self,package):
        check_crash = Check_system().check_all_crashes()
        check_devices=Check_system().check_device_status()
        check_package=Check_system().check_package_status(package)
        if check_devices == True and check_package == True:
            logger.info('Test no crash and system hang: PASS')
            return True
        else:
            logger.debug('Test has crash and system hang: FAIL')
            return False

    def rm_crash_file(self):
        self.remove_tomstones()
        self.remove_panic_file()

check_system = Check_system()