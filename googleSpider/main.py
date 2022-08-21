from operator import truediv
from urllib import response
import requests
from lxml import html
import os
import asyncio
import aiofiles as aiof
import aiohttp
import tqdm
from typing import List
import time
import random
from bs4 import BeautifulSoup as bs
from requests.exceptions import ProxyError

import sqlite3

'AIzaSyA2HvtTC23IsDg1FppxnSyO4GxiHXve0jA'

conn = sqlite3.connect('google.db')
cursor = conn.cursor()

cursor.execute('create table IF NOT EXISTS docs (url varchar(2083) primary key, name varchar(2083), query varchar(50))')

def create_docUrl(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT OR IGNORE INTO docs(url, name, query)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

# google 搜索的sample url
# https://www.google.com/search?q=%E8%AF%95%E5%8D%B7+filetype%3Adoc

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

url = 'https://www.google.com/search'

# proxies = {
#     'http': 'http://127.0.0.1:1080',
#     'https': 'http://127.0.0.1:1080',
# }

uselessProxies = []


def get_free_proxies():
    url = "https://www.google-proxy.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    # for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
    for row in soup.find("table", attrs={"class": "table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            google = tds[5].text
            if google == 'yes':
                proxies.append(host)
        except IndexError:
            continue
    return proxies

real_free_proxies = get_free_proxies()

def get_filtered_proxies(useless_proxies):
    uselessProxies.append(useless_proxies)
    return [item for item in real_free_proxies if item not in uselessProxies]

def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxies)
    session.proxies = {"http": 'http://'+'80.48.119.28:8080', "https": 'https://'+'80.48.119.28:8080'}
    return session

# proxies = {
#     'http': 'http://205.155.45.111:3128',
#     'https': 'http://205.155.45.111:3128',
# }

# proxy = 'http://127.0.0.1:1080'


def storePreviewPages(response):
    """
    store the preview pages

    Args:
        response (_type_): _description_
    """
    page_text = response.text
    file_name = 'debug'+'.html'
    with open(file_name, 'w', encoding='utf-8') as fp:
        fp.write(page_text)


def extractDocs(query, response) -> List[str]:
    """
    _summary_

    Args:
        response (_type_): _description_

    Returns:
        List[str]: _description_
    """
    response_content = response.content
    root = html.fromstring(response_content)
    docs = []
    for i in range(1, 101):
        a = '//*[@id="rso"]/div[{0}]/div/div[1]/div/a'.format(i)
        h3 = '//*[@id="rso"]/div[{0}]/div/div[1]/div/a/h3'.format(i)
        try:
            a_href = root.xpath(a)[0].get('href')
            h3_text = root.xpath(h3)[0].text
            docs.append((a_href, h3_text, query))
        except:
            # print(i)
            continue
    return docs


def query_docIds_on_google(query, num=100, start=0):
    # 对指定url发起的请求url是携带参数的
    # 处理url所携带的参数，将其封装到字典当中
    # num is up to 100
    # start 是start from,也就是offset
    param = {
        #'q': query+' filetype:doc',
        'q': query +' filetype:doc OR filetype:docx',
        'oq': query +' filetype:doc OR filetype:docx',
        'num': num,
        'start': start,
        'filter': 0,
        'lr': 'lang_zh-CN'
    }
    # response = requests.get(url=url, params=param, headers=headers)
    # , proxies=proxies)
    proxies = get_free_proxies()
    session = get_session(proxies)

    # response = requests.get(url=url, params=param, headers=headers, proxies=proxies)
    # failed = True
    # while failed:
    #     try:
    #         response = session.get(url=url, params=param, headers=headers, timeout=1)
    #         failed = response.status_code != 200
    #     except:
    #         storePreviewPages(response)
    #         proxies = get_free_proxies()
    #         session = get_session(proxies)
            
    # try:
        
    # except:
    # while session.get(url=url, params=param, headers=headers).status_code != 200:
        # proxies = get_free_proxies()
        # session = get_session(proxies)
    #     response = session.get(url=url, params=param, headers=headers)
    # while response.status_code != 200:
    #     response = session.get(url=url, params=param, headers=headers, timeout=10)

    response = session.get(url=url, params=param, headers=headers, timeout=1)
    while response.status_code != 200:
        storePreviewPages(response)
        # proxies = get_free_proxies()
        new_proxies = get_filtered_proxies(session.proxies['http'])
        session = get_session(new_proxies)
        try:
            response = session.get(url=url, params=param, headers=headers, timeout=1)
        except ProxyError:
            pass

    docs = extractDocs(query, response)

    

    if start == 0:
        try:
            response_content = response.content
            root = html.fromstring(response_content)
            totalPages = len(root.xpath('//*[@id="botstuff"]//td')) - 2
            totalPages = 0 if totalPages < 0 else totalPages
            for i in tqdm.tqdm(range(1, totalPages)):
                time.sleep(1)
                docs.extend(query_docIds_on_google(query, num, i*100))
        except:
            print("Unable to get total pages!")
            print("query: {}".format(query))
            # storePreviewPages(response)
    return docs

async def async_download_doc(doc,
                             session: aiohttp.ClientSession,
                             sem: asyncio.Semaphore) -> None:
    doc_url = doc[0]
    dir_path = os.path.join(os.getcwd(), doc[2])
    isExist = os.path.exists(dir_path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(dir_path)
    doc_path = os.path.join(os.getcwd(), doc[2], str(doc[1])+".doc")
    if doc_url.endswith('.docx'):
        os.path.join(os.getcwd(), doc[2], str(doc[1])+".docx")

    # This timeout is useless.
    # timeout = aiohttp.ClientTimeout(total=30)
    # A workaround solution:
    # https://stackoverflow.com/a/64686124
    # https://github.com/aio-libs/aiohttp/issues/3203
    timeout = aiohttp.ClientTimeout(total=60, sock_connect=30, sock_read=30)

    async with sem:
        try:
            # async with session.get(doc_url, timeout=timeout, proxy=proxy) as response:
            async with session.get(doc_url, timeout=timeout) as response:
                if response.status != 200:
                    print("Unable to download doc {}!".format(doc[1]))
                    print("Status code: {}".format(response.status))
                # if int(response.headers['Content-length']) < 100000: # 100kb
                #     print("File is too small" + ": {}".format(response.headers['Content-length']))
                content = await response.read()
                async with aiof.open(doc_path, "wb") as fhand:
                    await fhand.write(content)
                    await fhand.flush()
        except Exception as e:
            print(e)

async def downloadDocs(docs, maximum_num_connections: int = 30):
    tasks = []
    sem = asyncio.Semaphore(30)

    connector = aiohttp.TCPConnector(
        limit_per_host=maximum_num_connections, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        for doc in docs:
            task = asyncio.create_task(
                async_download_doc(
                    doc,
                    session=session,
                    sem=sem,
                ))
            tasks.append(task)

        pbar = tqdm.tqdm(total=len(tasks))
        for f in asyncio.as_completed(tasks):
            value = await f
            pbar.set_description(value)
            pbar.update()
        # responses = [
        #     await f
        #     for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))
        # ]


def logTime(time_start, time_end):
    time_elapsed = time_end - time_start
    print("Download Time Elapsed: {:02d}:{:02d}:{:02d}".format(
        int(time_elapsed // 3600), int(time_elapsed % 3600 // 60),
        int(time_elapsed % 60 // 1)))

def read_queries_from_file(start = 0):
    file_path = os.path.join(os.getcwd(), 'bingSearch',"dict.txt")
    file1 = open(file_path, 'r', encoding='utf-8')
    Lines = file1.readlines()

    count = 0
    queries = []
    for line in Lines:
        count += 1
        queries.append(line.split('\t')[0])
    return queries[start:]


if __name__ == '__main__':
    start = 5
    queries = read_queries_from_file(start)

    fileCount = 0
    for i in range(len(queries)):
        # print query number
        print("querying: {}th query".format(i+start))
        print("query: {}".format(queries[i]))
        print("fileCount: {}".format(fileCount))
        time_start = time.time()
        docs = query_docIds_on_google(queries[i])
        fileCount += len(docs)
        time_end = time.time()
        logTime(time_start, time_end)
        for doc in docs:
            create_docUrl(conn, doc)
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(downloadDocs(docs))
        time_end2 = time.time()
        logTime(time_end, time_end2)