#-*-coding:UTF-8-*-
from utils import get_tree, filter_tags, filter_comment
from lxml import etree

Article_url = 'http://bbs.nankai.edu.cn/group/article/{}'

class Parse(object):
        
    def __init__(self,article_id, session):
        self._article_id = article_id
        self.tree = get_tree(Article_url.format(article_id), session)

    @property
    def article_id(self):
        return self._article_id

    def parse_article(self):
        d = dict()                
        #parse article title
        title = self.tree.xpath('//p[@class="article-title"]/text()')
        if title:
            d['article_title'] = title[0].encode('ISO-8859-1')
        else:
            d['article_title'] = 'no_title'
        #parse article author name
        d['author_name'] = self.tree.xpath('//a[contains(@class, "author-name author-info__detail")]/text() | //a[@class="author-info__detail"]//text()')[0].encode('ISO-8859-1')
        #parse article time
        d['article_time'] = self.tree.xpath('//p[@class="author-info__detail"]/text()')[0].encode('ISO-8859-1')
        #parse article content
        # d['article_content'] ='\r\n'.join([a.encode('ISO-8859-1') for a in self.tree.xpath('//div[@class="article-info"]//text()')])
        content_ele = self.tree.xpath('//div[@class="article-info"]')[0]
        #convert content_ele to string
        tmp = etree.tostring(content_ele,encoding='ISO-8859-1',method="html")
        # print tmp
        d['article_content'] = filter_tags(tmp)
        #print 'article_content type is:', type(d['article_content'])
        return d
 
    def parse_comment(self):
        comments = []
        xpath = '/html/body/div[@id="main"]/div[@id="left"]/div[@id="reviews-tab"]/div[@class="reviews"][1]'
        reviews = self.tree.xpath(xpath)
        # print 'reviews number:%d' %len(reviews)
        for ele_ in reviews[0].iterchildren():
            if ele_.attrib["class"] == 'review':
                comments.append(filter_comment(ele_))
        return comments
