# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      jinja2html
    Description:    
    Author:         wanglin
    Date:           2017/12/28
--------------------------------------------
    Change Activity:2017/12/28;
--------------------------------------------
"""
__author__ = 'wanglin'

import os
from jinja2 import Environment, FileSystemLoader
from util.LogHandler import LogHandler

log = LogHandler('jinja2html')
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def create_html(nameinfo, datainfo, tableinfo):
    context = {
        'info': nameinfo,
        'datainfo': datainfo,
        'tableinfo': tableinfo
    }
    log.info('Jinja1 context info: {}'.format(context))
    html = TEMPLATE_ENVIRONMENT.get_template('base.html').render(context)
    log.info('Successful rendering report page. ')
    return html
