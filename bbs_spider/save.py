#coding:utf-8
from spider.parser import Parse
from log.log import log
import requests,sqlite3
import sys

def load_save(article_id,connection,cursor,session):
    try:
        p = Parse(article_id,session)
        al = p.parse_article()
        ct = p.parse_comment()
        #article data to be inserted
        a_data = (article_id, al['article_title'], al['author_name'], al['article_time'], al['article_content'])
        cursor.execute('''INSERT INTO article VALUES (?,?,?,?,?)''',a_data)
        #comment data to be inserted
        if len(ct)>0:
            c_data = [(article_id,ele['review_author__name'],ele['review_author__date'],ele['review_content']) for ele in ct]
            cursor.executemany('''INSERT INTO comment VALUES (?,?,?,?)''', c_data)
        #save process successed
        cursor.execute('''INSERT INTO process VALUES (?,?,?)''',(article_id,1,None))
        #connection.commit()
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        log.info('Network problem, sys exit')
        log.close()
        cursor.close()
        connection.close()
        sys.exit()
    except requests.HTTPError as e:
        #save process failed
        cursor.execute('''INSERT INTO process VALUES (?,?,?)''',(article_id,0,e.message[:3]))
    except (KeyboardInterrupt,SystemExit) as e:
        connection.rollback()
        cursor.execute('''INSERT INTO process VALUES (?,?,?)''',(article_id,2,None))
        connection.commit()
        log.info("KeyboardInterrupt, sys exit")
        log.close()
        cursor.close()
        connection.close()
        sys.exit()
    except sqlite3.Error as e:
        try:
            connection.rollback()
        finally:
            log.info("sqlite error, sys exit")
            log.close()
            cursor.close()
            connection.close()
            sys.exit()
    except:
        pass
