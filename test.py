# import re
# pub_time = '. 2019 Aug;43(4):490-496. doi: 10.5535/arm.2019.43.4.490. Epub 2019 Aug 31.'
# pub_time = re.search(r'\d{4}\s[a-zA-Z]{3}', pub_time).group()
# print(pub_time)
import requests
#导入bs4模块
from bs4 import BeautifulSoup
from lxml import html
import re
import time
from pprint import pprint

url="https://www.ncbi.nlm.nih.gov/pubmed/"
pmid = str(31499603)
url = url + pmid
try:
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
            "Chrome/44.0.2403.157 Safari/537.36 "
    headers = {"User-Agent": user_agent,
                "Connection": "keep-alive"}
    r = requests.get(url, timeout=300, headers=headers)
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

    abstract = []
    parent = soup.find('div', class_='abstr')
    for i in parent.contents:
        for j in i.contents:
            if not isinstance(j, str):
                abstract.append(j.contents[0])
            else:
                abstract.append(j)
    abstract = "\n".join(abstract)
except:
    print('wrong')
    pass
print(abstract)