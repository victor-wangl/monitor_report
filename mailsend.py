# -*- coding: utf-8 -*-
"""
-------------------------------------------
    File Name:      mailsend
    Description:    
    Author:         wanglin
    Date:           2017/12/28
--------------------------------------------
    Change Activity:2017/12/28;
--------------------------------------------
"""
__author__ = 'wanglin'

import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 引入外部文件
from jinja2html import create_html
from monitorSpider import get_info
from util.LogHandler import LogHandler
from util.DBManager import get_table_count

log = LogHandler('mailsend')
_sender_address = 'wanglin@ruifucredit.com'
_reciver_address = 'wanglin@ruifucredit.com,luoyunfei@ruifucredit.com,wangyuanguo@ruifucredit.com,zhangyao@ruifucredit.com,taoliangpeng@ruifucredit.com'
_subject = u'平台报告-【%s】' % datetime.datetime.now().strftime('%Y-%m-%d')
_passwd = '3Edc4rfv'
_smtpadd = 'smtp.ruifucredit.com'


def sendMail(sender, reciver, subject, content, passwd, smtpadd):
    log.info('Start to initialize the mail message.')
    username = sender
    password = passwd
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    # html格式
    html = content
    htm = MIMEText(html, 'html', 'utf-8')
    msg.attach(htm)
    msg['From'] = sender
    msg['To'] = reciver

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpadd)
    smtp.login(username, password)
    smtp.sendmail(sender, reciver.split(','), msg.as_string())
    smtp.quit()


if __name__ == "__main__":
    result = get_info()
    tableinfo = get_table_count()
    html = create_html(result['nameinfo'], result['datainfo'], tableinfo)
    sendMail(_sender_address, _reciver_address, _subject, html, _passwd, _smtpadd)
    log.info('Send mail successfully.')
