#!/usr/bin/env
#import utils
import psutil
import msgpack
import time
import socket
import requests
import datetime
import logging

WEB_URL = "http://localhost:5001/"

get_name = lambda: socket.gethostname()
get_milli = lambda: int(round(time.time() * 1000))
get_time = lambda: str(datetime.datetime.now())
logger = logging.getLogger()

from abc import ABCMeta, abstractmethod

"""
class Msg(object):
    def __init__(self, name, data)
        self.name = name
        self.data = data

    def encode(self):
        ret = { 'name': self.name,
                'data': msgpack.packb(self.data)}
        return msgpack.packb(ret)
"""


class Plugin(object):
    __metaclass__ = ABCMeta
    _name = 'Plugin'

    @abstractmethod
    def load_config(self): 
        pass

    @abstractmethod
    def run(self): 
        pass
    
    @staticmethod
    @abstractmethod
    def create_blank_config(self):
        pass

    def encode(self):
        ret = {'name': self._name,
               'time': get_time(),
               'epoch_milli': get_milli(),
               'host': get_name(),
               'data': msgpack.packb(self.run())}
        return msgpack.packb(ret)

    @staticmethod
    @abstractmethod
    def decode(msg):
        pass

    @staticmethod
    @abstractmethod
    def push(msg):
        pass


class LogPlugin(Plugin):
    """ Watch log files for regex matches """
    _name = 'LOGPlugin'
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()

    def load_config(self):    
        pass

    @staticmethod
    def create_blank_config(self):
        return {
                "meta": {
                    "update": 60000
                    },
                "cpu": {},
                "load": {}
                }    


class CPUPlugin(Plugin):
    """ Watch CPU Percentages and Load"""
    _name = 'CPUPlugin'
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.load_config()

    @staticmethod
    def create_blank_config(self):
        return {
                "meta": {
                    "update": 30000
                    },
                "cpu": {},
                "load": {}
                }    

    def load_config(self):
        pass
    
    @staticmethod
    def decode(msg):
        CPUPlugin.push(msg)

    @staticmethod
    def push(data):
        url = WEB_URL + 'cpu/' + data['host']
        d = msgpack.unpackb(data['data'])
        d['timestamp'] = str(data['time'])
        d['epoch_milli'] = data['epoch_milli']
        d['CPU'] = str(d['CPU'])
        try:
            r = requests.post(url, data=d)
        except Exception as e:
            logger.error("Caught error when posting back data: %s", e)

    def run(self):
        ret = {}
        with open('/proc/loadavg', 'r') as f:
            temp = f.read().split()[:3]
            ret['load_1'] = temp[0]
            ret['load_5'] = temp[1]
            ret['load_15'] = temp[2]
        ret['CPU'] = psutil.cpu_percent(percpu=True)
        return ret


