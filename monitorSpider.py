# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      monitorSpider
    Description:    
    Author:         wanglin
    Date:           2017/12/28
--------------------------------------------
    Change Activity:2017/12/28;
--------------------------------------------
"""
__author__ = 'wanglin'

import json
import requests
import datetime
from util.LogHandler import LogHandler

log = LogHandler('monitorSpider')


name = {'Total': '-', 'Used': '-', 'Free': '-', 'PercentUsed': '-', 'TotalBlocks': '-', 'TotalFiles': '-',
        'SoftwareVersion': '-'}

node = {'name': '-', 'lastContact': '-', 'xferaddr': '-', 'adminState': '-', 'capacity': '-', 'usedSpace': '-',
        'blockPoolUsedPercent': '-', 'version': '-', }


def get_info():
    url = 'http://12.3.10.190:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo'
    try:
        r = requests.get(url=url)
    except Exception as ex:
        print(ex)
        url = url.replace('120', '130')
        r = requests.get(url=url)
    result = dict()
    content = json.loads(r.content)
    names = []
    nodes = []
    if 'beans' in content:
        datas = content['beans']
        for data in datas:
            if 'Total' in data:
                log.info('Successful access to the cluster information.')
                monitor = name
                monitor['Total'] = '%.2fGB' % round(data['Total'] / 1024 / 1024 / 1024, 2)
                monitor['Used'] = '%.2fGB' % round((data['Used'] + data['NonDfsUsedSpace']) / 1024 / 1024 / 1024, 2)
                monitor['Free'] = '%.2fGB' % round(data['Free'] / 1024 / 1024 / 1024, 2)
                monitor['PercentUsed'] = '%.2f%%' % round(100 - data['PercentRemaining'], 2)
                monitor['TotalBlocks'] = data['TotalBlocks']
                monitor['TotalFiles'] = data['TotalFiles']
                monitor['SoftwareVersion'] = data['SoftwareVersion']
                names.append(monitor)
                log.info('Cluster information: {}'.format(names))
                # 存活节点
                LiveNodes = json.loads(data['LiveNodes'])
                for key, value in LiveNodes.items():
                    nodeItem = node.copy()
                    nodeItem['name'] = key
                    nodeItem['lastContact'] = value['lastContact']
                    nodeItem['xferaddr'] = value['xferaddr'].split(':')[0]
                    nodeItem['adminState'] = value['adminState']
                    nodeItem['capacity'] = '%.2fGB' % round(value['capacity'] / 1024 / 1024 / 1024, 2)
                    nodeItem['usedSpace'] = '%.2fGB' % round(value['usedSpace'] / 1024 / 1024 / 1024, 2)
                    nodeItem['remaining'] = '%.2fGB' % round(value['remaining'] / 1024 / 1024 / 1024, 2)
                    nodeItem['blockPoolUsedPercent'] = '%.2f%%' % round(value['blockPoolUsedPercent'], 2)
                    nodeItem['version'] = value['version']
                    log.info('LiveNode information: {}'.format(nodeItem))
                    nodes.append(nodeItem)

                # 挂掉节点
                DeadNodes = json.loads(data['DeadNodes'])
                for key, value in DeadNodes.items():
                    nodeItem = node
                    nodeItem['name'] = key
                    seconds = value['lastContact']
                    lastContact = datetime.datetime.now().timestamp() - int(seconds)
                    nodeItem['lastContact'] = datetime.datetime.fromtimestamp(lastContact)
                    nodeItem['xferaddr'] = value['xferaddr'].split(':')[0]
                    nodeItem['adminState'] = value['decommissioned']
                    log.info('DeadNode information: {}'.format(nodeItem))
                    nodes.append(nodeItem)

    result['datainfo'] = nodes
    result['nameinfo'] = monitor
    return result
