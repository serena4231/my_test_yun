#!usr/bin/env python
#-*-coding:utf-8-*-

import subprocess
from logger import logger
import zipfile
import tarfile
import os
from logger import Logger
import threading
import signal
import traceback
import time
import sys

 
class Flashfile(object): 
    def __init__(self,path):
        self.mkdir(path)  
 
    def extract_flash_file(self, flash_file,pwd = None):
        
        # flash_file type:"C:\\Users\\flash.zip"
        filename, file_extension = os.path.splitext(flash_file)
 
#         # First unzip flash file if needed
        if zipfile.is_zipfile(flash_file):
            try:
                zip_file = zipfile.ZipFile(flash_file, "r")
                logger.info("FlashManager: unzip flash file (%s)" % flash_file)
                zip_file.extractall(filename,pwd = pwd)
                zip_file.close()
#                 flash_file_to_use = flash_file
            except Exception as ex:
                err_msg = "FlashManager: Flash input file %s, unzip issue, error : %s" % (flash_file, str(ex))
                logger.error(err_msg)
        elif tarfile.is_tarfile(flash_file):
            try:
                tar_file = tarfile.open(flash_file, "r")
                logger.info("untar flash file (%s)" % flash_file)
                tar_file.extractall(filename,pwd = pwd)
                tar_file.close()
#                 flash_file_to_use = flash_file
            except Exception as ex:
                err_msg = "FlashManager: Flash input file %s, untar issue, error : %s" % (flash_file, str(ex))
                logger.error(err_msg)
        elif file_extension.lower() == ".xml" or file_extension.lower() == ".bin":
            if os.path.isfile(flash_file):
                logger.info("FlashManager: Flash file %s exists" % flash_file)
#                 flash_file_to_use = flash_file
            else:
                err_msg = "Flash file %s not found!" % flash_file
                self._logger.error(err_msg)
        else:
            err_msg = "lash file %s format is not suitable (.xml, .bin or .zip file should be used)" \
                      % str(flash_file)
            self._logger.error(err_msg)
#         return flash_file_to_use
    
    def mkdir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)  
            logger.info('create the file')

class Command(object):
    """
    subprocess commands in a different thread with TIMEOUT option.
    """
    command = None
    process = None
    status = None
    output, error = '', ''

    def __init__(self, command):
        self.command = command

    def start(self, timeout=None, **kwargs):
        """ Run a command then return: (status, output, error). """
        def target(**kwargs):
            """run target"""
            try:
                self.process = subprocess.Popen(self.command,shell=True, **kwargs)
                self.output, self.error = self.process.communicate()
                logger.info('{0}'.format(repr(self.output)))
                self.status = self.process.returncode
            except:
                self.error = traceback.format_exc()
                self.status = -1
        # default stdout and stderr
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        # thread
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.kill_proc(self.process.pid)
            thread.join()
            logger.info('kill')
        return self.status, self.output, self.error
 
    @staticmethod
    def kill_proc(pid):
        """kill process"""
        try:
            # os.system("TASKKILL /F /T /PID {pid}".format(pid=pid)) kill windows

            os.killpg(os.getpgid(pid),signal.SIGTERM)
        except OSError:
            pass


def check_adb_device():

    # Wait a few seconds before checking
    logger.debug("Checking for adb connection, please wait:")
    time.sleep(1)

    # Failure flag
    adb_dev_ok = False

    # Send command to check for devices
    proc = subprocess.Popen("adb -host devices",
        stdout=subprocess.PIPE,shell=True)
    (out,err) = proc.communicate()
    
    # Check the return string
    #python3.x need to encode str type
    if out.find('8'.encode()) > -1:
        adb_dev_ok = True
        logger.debug("Device found with adb!")
    else:
        adb_dev_ok = False
        raise Exception("Cannot detect the device through adb.")

    return adb_dev_ok


