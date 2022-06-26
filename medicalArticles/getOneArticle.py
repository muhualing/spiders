import requests
#导入bs4模块
from bs4 import BeautifulSoup
from lxml import html
import re
import time
from Article import Article

def getHtmlByPmid(pmid):
    url = "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pmid)
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

def getOneArticleByPmid(pmid=31499603):
    r = getHtmlByPmid(pmid=pmid)
    article = Article()
    # Article().printAll()
    print('-'*100)
    try:
        root = html.fromstring(r)
        soup = BeautifulSoup(r,'lxml')

        article.title = root.xpath('//*[@id="maincontent"]/div/div[5]/div/h1/text()')[0]

        article.author = soup.select('#maincontent > div > div.rprt_all > div > div.auths')[0].text

        pub_time_selector = soup.select('#maincontent > div > div.rprt_all > div > div.cit')
        pub_time_text = ""
        if pub_time_selector != []:
            pub_time_text = pub_time_selector[0].text
        if re.search(r'\d{4}\s[a-zA-Z]{3}', pub_time_text) is not None:
            article.pub_time = re.search(r'\d{4}\s[a-zA-Z]{3}', pub_time_text).group()

        article.pmid = pmid
        
        # 疾病类型写死在article里面了
        # article.type = 'Autism' 

        # keywords 有些有 有些没有，需要在abstract里面去正则匹配
        article.keywords = ""

        parent = soup.find('div', class_='afflist')
        author_info = []
        if parent is not None:
            for i in parent.contents[1].contents:
                if len(i.contents[0]) > 10:
                    author_info.append(i.contents[0])
            author_info = "\n".join(author_info)
        else:
            author_info = ""
        article.author_info = author_info

        abstract = ""
        parent = soup.find('div', class_='abstr')
        if parent is not None:
            res = [s for s in list(parent.descendants) if isinstance(s, str)]
            abstract = "\n".join(res)
        article.abstract = abstract
        parent = soup.find('div', class_='keywords')
        if parent is not None:
            article.keywords = parent.contents[1].contents[0]
        else:
            article.keywords = ""
        article.create_time = time.time()
        article.update_time = time.time()
        article.printAll()
        return article
    except:
        return "Something Wrong!"