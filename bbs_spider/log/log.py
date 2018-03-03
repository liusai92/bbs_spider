#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

class log(object):
    def __init__(self):
        self.fileobj = open('./nkbbs_spider/log/spider.log','ab')
    def info(self, msg):
        timestamp = '['+str(datetime.today())+']'
        self.fileobj.write(timestamp + ' ' + msg + '\n')
    def close(self):
        self.fileobj.close()

log = log()
