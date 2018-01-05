# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      ConfigHandler
    Description:    
    Author:         wanglin
    Date:           2018/1/3
--------------------------------------------
    Change Activity:2018/1/3;
--------------------------------------------
"""
__author__ = 'wanglin'

import os
import sys
from configobj import ConfigObj

class ConfigHandler(object):

    def __init__(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(os.path.split(path)[0], 'db.ini')
        self.config = ConfigObj(config_path, encoding='UTF-8')

    def get(self, option):
        param = dict()
        try:
            for key in self.config[option]:
                param[key] = self.config[option][key]
        except Exception as ex:
            print('{} is not found, please input the right option' .format(ex))
        return param

    def get_value(self, option, key):
        return self.config[option][key]

    def set_value(self, option, key, value):
        self.config[option][key] = value
        self.config.write()

if __name__ == '__main__':
    config = ConfigHandler()
    print(config.get('oracle'))