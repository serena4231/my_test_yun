#!usr/bin/env python
#coding:utf-8

'''
create on 2016.11.23
@author qianqian，huang

'''

import time
import binascii

import serial
from serial import SerialException

from logger import logger

WAIT_ON_OFF = {
            "PRESS": 0.2,
            "ON": 3,
            "OFF": 15,
            "FASTBOOT": 15,
            "DNX": 15
            }
WAIT_ACTION = {
            "PRESS": 0.2,
            "ON": 10,
            "OFF": 15,
            "FASTBOOT": 10,
            "DNX": 10
            }


class Relay(object):
    def __init__(self, portName, timeout=0, writeTimeout=0):
        self.portName = portName
        self.__serialConfig = {'port': portName,
                               'baudrate': 19200,
                               'bytesize': 8,
                               'timeout': timeout,
                               'writeTimeout':writeTimeout,
                               }
        self.ser = None
	print 'self.ser',self.ser
        self.open()

    def open(self):
        try:
            self.ser = serial.Serial(**self.__serialConfig)
	    print 'self.ser', self.ser
        except SerialException as msg:
            logger.debug("Exception: %s" % msg)
            logger.debug('Result:failed')


    def close(self):
        '''close the serial port'''
        if self.ser:
            self.ser.close()
            logger.info('finished the close')
            self.ser = None

    def write(self,data):
        length = self.ser.write(binascii.a2b_hex(data))
        return length


    def on_off(self,timeout,relay_port):
        length =0
        if self.ser is None:
            self.open()
        try:
            length = self.write(relay_port)
            time.sleep(timeout)
        except SerialException as msg:
            logger.debug("Exception: %s" % msg)
            logger.debug('Result:failed')
            return length



class Relayed_device(Relay):
    '''
power_on = ['65','66','67','68','69','6A','6B','6C']
power_of = ['6F','70','71,'72','73','74','75','76']

'''

    def __init__(self,
                 relay_port = None,
                 power_port = None,
#                  v_up_port = None,
                 v_down_port = None):
#         if relay_port:
#             self.relay = Relay(portName = relay_port)
#             self.power_port = power_port
# #             self.v_up_port = v_up_port
#             self.v_down_port = v_down_port
#
#         else:
#             self.relay = None
        self.power_port = power_port
#             self.v_up_port = v_up_port
        self.v_down_port = v_down_port
        super(Relayed_device,self).__init__(portName=relay_port)


    def press_power(self):
        self.on_off(WAIT_ON_OFF["PRESS"], self.power_port)
        time.sleep(WAIT_ACTION["PRESS"])

    def long_press_power(self):
        self.on_off(WAIT_ON_OFF["ON"], self.power_port)
        time.sleep(WAIT_ACTION["PRESS"])

    def long_press_power_shutdown(self, long_press_time = 15):
        self.on_off(long_press_time, self.power_port)
        time.sleep(WAIT_ACTION["PRESS"])

    def press_volume_up(self):
        self.on_off(WAIT_ON_OFF["PRESS"], self.v_up_port)
        time.sleep(WAIT_ACTION["PRESS"])

    def press_volume_down(self):
        self.on_off(WAIT_ON_OFF["PRESS"], self.v_down_port)
        time.sleep(WAIT_ACTION["PRESS"])

    def power_on(self):
        self.on_off(WAIT_ON_OFF["ON"], self.power_port)
        time.sleep(WAIT_ACTION["ON"])

    def power_off(self):
        self.on_off(WAIT_ON_OFF["OFF"], self.power_port)
    	time.sleep(WAIT_ACTION["PRESS"])

    def enter_dnx(self):
        self.on_off(10,self.v_down_port)
        self.on_off(5,self.power_port)
        time.sleep(WAIT_ON_OFF["DNX"])

    def close_dnx(self):
        self.on_off(WAIT_ON_OFF["PRESS"], self.v_down_port)
        self.on_off(WAIT_ON_OFF["PRESS"], self.power_port)



