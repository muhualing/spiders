import pymysql
from functools import wraps
from Article import Article
def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class MySQLProvider(object):
    def __init__(self, host="localhost", port=3306, user='root', password='root', db='articles', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def getAllArticles(self):
        # 打开数据库连接
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, 
                password=self.password, db=self.db, charset=self.charset)
        
        # 获取游标
        cursor = db.cursor()

        # 执行sql语句
        SQL_getAllAriticles = "SELECT * FROM " + self.db + ".article;"
        cursor.execute(SQL_getAllAriticles)

        # 获取所有文章
        raw_articles = cursor.fetchall()
        articles = {}
        for raw_article in raw_articles:
            article = Article(*(raw_article[1:]))
            if article.pmid not in articles:
                articles[article.pmid] = article
        db.close()
        return articles
    
    def saveArticles(self, articles):
        # 打开数据库连接
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, 
                password=self.password, db=self.db, charset=self.charset)

        # 获取游标
        cursor = db.cursor()

        
        # SQL 插入语句
        SQL = "insert into article(title, author, pub_time, pmid, type,\
                            keywords, author_info, create_time, update_time, abstract) \
                            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            for article in articles.values():
                parm = (article.title, article.author, article.pub_time, int(article.pmid), article.type,\
                        article.keywords, article.author_info, article.create_time, article.update_time, article.abstract)
                # 执行sql语句
                cursor.execute(SQL, parm)
                # 提交到数据库执行
                db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        db.close()

# 测试数据库功能的代码
# 爬取一个文章，并将其插入数据库。
# from getOneArticle import getOneArticleByPmid
# article = getOneArticleByPmid()
# articles = {}
# articles[article.pmid] = article
# mysqlProvider = MySQLProvider()
# old_articles = mysqlProvider.getAllArticles()
# mysqlProvider.saveArticles(articles)