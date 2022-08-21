import json
import os 
from pprint import pprint
import requests
import time
import asyncio
import aiofiles as aiof
import aiohttp
import tqdm
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('create table IF NOT EXISTS docs (url varchar(2083) primary key, query varchar(50))')


def create_docUrl(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT OR IGNORE INTO docs(url,query)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid


subscription_key = 'a30ffde4947443b1bd28f3a1a46fc32c'
endpoint = 'https://api.bing.microsoft.com/v7.0/search'

headers = { 
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Accept-Language': 'zh-CN',
}

def query_docUrls_on_bing(query, offset=1):
    # Construct a request
    mkt = '	zh-CN'
    params = { 
        'q': query + " filetype:doc OR filetype:docx", 
        'mkt': mkt, 
        'count': 50,
        'setLang': 'zh-CN',
        'cc': 'CN',
        'offset': offset,
    }

    tasks = []

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_response = response.json()
        totalResults = search_response['webPages']['totalEstimatedMatches']
        search_results = search_response['webPages']['value']
        urls = [o['url'] for o in search_results]
        for url in urls:
            tasks.append((url, query))
        if offset < totalResults:
            time.sleep(0.33)
            tasks += query_docUrls_on_bing(query, offset + 50)
    except Exception as ex:
        raise ex
        # print(ex)
    return tasks

# read queries from file
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

# 最多有几个异步函数等待
sem = asyncio.Semaphore(20)

if __name__ == '__main__':
    # docs = query_docUrls_on_bing('合同', 1)
    start = 0

    queries = read_queries_from_file(start)

    fileCount = 0
    # queries = ["试卷"]
    for i in tqdm.tqdm(range(len(queries))):
        print("querying: {}th query".format(i+start))
        print("query: {}".format(queries[i]))
        print("fileCount: {}".format(fileCount))
        time_start = time.time()
        tasks = query_docUrls_on_bing(queries[i], 1)
        for task in tasks:
            create_docUrl(conn, task)
        fileCount += len(tasks)
        print("fileCount: {}".format(fileCount))
        # time_end = time.time()
        # logTime(time_start, time_end)
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(downloadDocs(docs))
        # time_end2 = time.time()
        # logTime(time_end, time_end2)