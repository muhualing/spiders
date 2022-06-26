from getAllPmidsByTerm import getAllPmidsByTerm
from getOneArticle import getOneArticleByPmid
from MySQLProvider import MySQLProvider
def crawl(test=False, incremental=False):
    # 数据库管理实例
    mysqlProvier = MySQLProvider()
    # 获取所有与term相关的pmid
    pmids = getAllPmidsByTerm(test=test, incremental = incremental)

    # 去重，避免重复插入
    old_articles = mysqlProvier.getAllArticles()
    for pmid in old_articles:
        if pmid in pmids:
            pmids.remove(pmid)
    articles = {}
    bugPmid = []
    for pmid in pmids:
        # 对每一个pmid去爬取相应的数据存入article对象
        article = getOneArticleByPmid(pmid)
        if isinstance(article, str):
            bugPmid.append(pmid)
        else:
            # articles[article.pmid] = article
            cur_article = {}
            cur_article[article.pmid] = article
            try:
                mysqlProvier.saveArticles(cur_article)
            except BaseException:
                bugPmid.append(pmid)
    print(bugPmid)
# crawl(test=True)

# mysqlProvier.saveArticles(articles)
# for pmid in ['31494566', '20301487', '31478758', '31478755', '31474663', '31468394', '31456437']:
#     try:
#         getOneArticleByPmid(pmid)
#     except BaseException:
#         print(pmid)
