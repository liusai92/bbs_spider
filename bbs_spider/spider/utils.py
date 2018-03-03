#!/usr/bin/env python
#-*-coding:UTF-8-*-

import requests, re
from lxml import etree
from HTMLParser import HTMLParser
from ..log.log import log
import pickle
import os
#from requests.utils import get_encodings_from_content
__file__ = os.path.abspath(__file__)
ROOTPATH = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
DATAPATH = os.path.join(ROOTPATH, 'nkbbs_spider', 'data')
TIMEOUT = 10


def test_cookies(cookies):
    url = "http://bbs.nankai.edu.cn/index.php/main"
    r = requests.get(url, cookies=cookies)   
    r.raise_for_status()
    if r.content.find('kepler')>=0:
        return True
    return False

def get_cookies():
    with open(os.path.join(DATAPATH, 'cookies'),'rb') as f:
        cookies = pickle.load(f)
    if not test_cookies(cookies):
        log.info("The saving cookies is invalid now, please update cookies file in ./data")
        sys.exit()
    return cookies

def get_tree(url,session):
    r = session.get(url)
    r.raise_for_status()
    return etree.HTML(r.text)

def filter_comment(element):
    #filter parsed comment box element, return a dictionary containing comment info
    comment_info = {}
    
    
    comment_info['review_author__name'] = '-->'.join([b.text.encode('ISO-8859-1') for b in element.findall('./div[@class="review-author"]/a')])
    
    comment_info['review_author__date'] = element.find('.//span[@class="review-author__date"]').text.encode('ISO-8859-1')
    tmp = etree.tostring(element.find('.//div[@class="review-info"]'),encoding='ISO-8859-1',method="html")
    comment_info['review_content'] = filter_tags(tmp)
    return comment_info

def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_img = re.compile('<img')#处理图像标签
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_p=re.compile('</p>')#分段标签
    # re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\r\n',s)#将br转换为换行
    s=re_p.sub('\r\n',s)#将</p>转换为换行
    s=re_img.sub('(img',s)#将图像标签的<img处理为(img,防止下一步被处理掉
    s=re_h.sub('',s) #去掉HTML 标签
    # s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('[\r\n]+')
    s=blank_line.sub('\r\n',s)
    #去掉多余制表符
    tab_key=re.compile('[\t]+')
    s=tab_key.sub('\t',s)
    s=Entity2Unicode(s) #替换实体
    # s=replaceCharEntity(s)#替换实体
    return s

def Entity2Unicode(htmlstr):
    htmlparser = HTMLParser()
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称
        ucode=htmlparser.unescape(entity.decode('ISO-8859-1')).encode('utf-8')
        re_subedEntity=re.compile(entity)
        if ucode != entity:
            htmlstr=re_subedEntity.sub(ucode,htmlstr,1)
        else:
            htmlstr=re_subedEntity.sub('',htmlstr,1)
        sz=re_charEntity.search(htmlstr)
    return htmlstr
##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
   
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
