# monitor_report

    为了简单的监控集群的运行状况，写了一个小项目，主要是监控Hadoop集群运行状况，还有每天抽取数据的几张业务表数据总量监控，还有一个简单的页面渲染和邮件发送功能，用requests去请求hadoop集群50070web页面，用jinja2去渲染页面，还有smtplib发送邮件
