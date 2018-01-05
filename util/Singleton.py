# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      Singleton
    Description:    
    Author:         wanglin
    Date:           2018/1/3
--------------------------------------------
    Change Activity:2018/1/3;
--------------------------------------------
"""
__author__ = 'wanglin'

class Singleton(type):
    """
    Singleton Metaclass
    """

    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args)
        return cls._inst[cls]