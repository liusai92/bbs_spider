#coding = 'utf-8'
#this script is for creating database

import sqlite3

conn = sqlite3.connect('NKBBS.db')
c = conn.cursor()

#creat article table and comment table 
c.execute('''CREATE TABLE article
    (
    article_id int NOT NULL,
    article_title varchar NOT NULL,
    author_name char(15) NOT NULL,
    article_time datetime NOT NULL,
    article_content varchar NOT NULL,
    PRIMARY KEY (article_id)
    )''')
c.execute('''CREATE TABLE comment
	(article_id int NOT NULL,
     review_author__name char(35) NOT NULL,
     review_author__date datetime NOT NULL,
     review_content varchar NOT NULL,
     FOREIGN KEY (article_id) REFERENCES article(article_id)
     )''')
c.execute('''CREATE TABLE process
      (article_id int NOT NULL,
       status int default 2,  
       fail_reason varchar,
       PRIMARY KEY (article_id)
       )''')
#status must be in range 0,1,2 where 0:failed 1:sussessed 2:pending
#c.execute('''CREATE TABLE picture
#        (article_id int NOT NULL,
#        source char(30) NOT NULL,
#        image BLOB      NOT NULL,
#        FOREIGN KEY (article_id) REFERENCES article(article_id)
#        )''')
conn.close()
