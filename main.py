import requests
#导入bs4模块
from bs4 import BeautifulSoup
from lxml import html
import re
import time
from pprint import pprint
class Article(object):
    def __init__(self):
        # 标题
        self.title = ""
        # 中文简介
        self.author = ""
        # 发布时间
        self.pub_time = ""
        # 文献id
        self.pmid = None
        # 疾病类型
        self.type = ""
        # 关键词
        self.keywords = ""
        # 作者信息
        self.author_info = ""
        # 创建时间
        self.create_time = None
        # 更新时间
        self.update_time = None
        # 摘要
        self.abstract = None
    def printAll(self):
        pprint(self.__dict__)

def getHtml(url="https://www.ncbi.nlm.nih.gov/pubmed/",term="?term=Autism"):
    url = url + term
    try:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/44.0.2403.157 Safari/537.36 "
        headers = {"User-Agent": user_agent,
                    "Connection": "keep-alive"}
        r = requests.get(url, timeout=100, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content
    except:
        return "Something Wrong!"

def getKeywordsAndAuthorInfo(pmid):
    url="https://www.ncbi.nlm.nih.gov/pubmed/"
    url = url + pmid
    try:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/44.0.2403.157 Safari/537.36 "
        headers = {"User-Agent": user_agent,
                    "Connection": "keep-alive"}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        root = html.fromstring(r.content)
        keywords = root.xpath('//*[@id="maincontent"]/div/div[5]/div/div[5]/p/text()')[0]
        soup = BeautifulSoup(r.content,'lxml')
        parent = soup.find('dl')
        author_info = []
        for i in parent.contents:
            if len(i.contents[0]) > 10:
                author_info.append(i.contents[0])
        author_info = "\n".join(author_info)
        # author_info = root.xpath('//*[@id="maincontent"]/div/div[5]/div/div[3]/div/dl')

        abstract = []
        parent = soup.find('div', class_='abstr')
        for i in parent.contents:
            for j in i.contents:
                if not isinstance(j, str):
                    abstract.append(j.contents[0])
                else:
                    abstract.append(j)
        abstract = "\n".join(abstract)
        return keywords, author_info, abstract
    except:
        return "Something Wrong!"
r = getHtmlText()
root = html.fromstring(r)
article = Article()
article.printAll()
print('-'*50)
try:
    title = root.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/p/a')[0].text
    author = root.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[1]/p[1]')[0].text
    pub_time = root.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[1]/p[2]/text()')[0]
    # pub_time = '. 2019 Aug;43(4):490-496. doi: 10.5535/arm.2019.43.4.490. Epub 2019 Aug 31.'
    pub_time = re.search(r'\d{4}\s[a-zA-Z]{3}', pub_time).group()
    # pub_time = 2019 Aug
    # 文献id
    pmid = root.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[2]/div/dl/dd')[0].text
    # 疾病类型
    term = "Autism"
    keywords, author_info, abstract = getKeywordsAndAuthorInfo(pmid=pmid)
    # # 关键词
    # self.keywords = ""
    # # 作者信息
    # self.author_info = ""
    # # 创建时间
    # self.create_time = ""
    # # 更新时间
    # self.update_time = ""
    article.title = title
    article.author = author
    article.pub_time = pub_time
    article.pmid = pmid
    article.type = term
    article.keywords = keywords
    article.author_info = author_info
    article.create_time = time.time()
    article.update_time = time.time()
    article.abstract = abstract
except expression as identifier:
    pass
article.printAll()
# soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())