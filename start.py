#!/usr/bin/env python
# coding:utf-8
import pickle
import sys
from bbs_spider.log.log import log
from bbs_spider.run import runSpider
import os
__file__ = os.path.abspath(__file__)
ROOTPATH = os.path.join(os.path.dirname(__file__))
DATAPATH = os.path.join(ROOTPATH, 'bbs_spider', 'data')


PerFetchNum = 1000

try:
    with open(os.path.join(DATAPATH, "startn"), "rb") as f:
        StartNum = pickle.load(f)
except:
    log.info("failure to load StartNum, be sure ./startn exists")
    sys.exit()

log.info("start fetch number {} to {} articles".format(StartNum, StartNum + PerFetchNum -1))
runSpider(StartNum, PerFetchNum)
log.info("sussess fetch number {} to {} articles".format(StartNum, StartNum + PerFetchNum -1))
with open(os.path.join(DATAPATH, 'startn'), "wb") as f:
    pickle.dump(StartNum + PerFetchNum, f)
log.info("sussess dump next StartNum {}".format(StartNum+PerFetchNum))
log.close()
