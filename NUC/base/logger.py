#!usr/bin/env python
#coding:utf-8
import logging
import os
import time

format_dict= {"DEBUG": logging.Formatter('%(asctime)s %(filename)s [func:%(funcName)s][line:%(lineno)d] %(levelname)s %(message)s')}

class Logger():
    ##create logger
    __cur_logger = logging.getLogger()
    ##create file path
    temp_dir= r"/home/buildbot/log"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    def __init__(self,loglevel,filename=''):
        timestamp= time.strftime("%Y-%m-%d-%H-%M-%S")   
        new_logger = logging.getLogger(__name__)
        new_logger.setLevel(logging.DEBUG)
        filename = filename or os.path.join(Logger.temp_dir,'peacock_build_{0}_{1}.log'.format(loglevel,timestamp))
        filehandler = logging.FileHandler(filename)
        filehandler.setLevel(logging.DEBUG)
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.DEBUG)
        formatter = format_dict[loglevel]
        filehandler.setFormatter(formatter)
        streamhandler.setFormatter(formatter)
        new_logger.addHandler(filehandler)
        new_logger.addHandler(streamhandler)
        Logger.__cur_logger = new_logger


    @classmethod
    def getlogger(cls):
        return cls.__cur_logger



logger = Logger("DEBUG").getlogger()
