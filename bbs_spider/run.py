#!/usr/bin/env python
# coding:utf-8

import sqlite3
from save import load_save
from spider.utils import get_cookies
from requests import Session
from requests.cookies import cookiejar_from_dict
# set start and end article_id and step transcation
import os
__file__ = os.path.abspath(__file__)
ROOTPATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
DATAPATH = os.path.join(ROOTPATH, 'nkbbs_spider', 'data')

def runSpider(StartNumber, PerFetchNumber):
    start = StartNumber
    end = StartNumber + PerFetchNumber
    step = 50
    with Session() as s:
        s.cookies = cookiejar_from_dict(get_cookies())
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        conn = sqlite3.connect(os.path.join(DATAPATH, 'NKBBS.db'), isolation_level = None)
        conn.text_factory = str
        c = conn.cursor()
        for article_id in range(start,end):
            if (article_id-start)%step==0:
                conn.commit()
                c.execute("BEGIN TRANSACTION")
                print article_id
            load_save(article_id,conn,c,s)
        conn.commit()
        c.close()
        conn.close()

