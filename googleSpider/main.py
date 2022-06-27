from ssl import VerifyMode
import requests
from lxml import html
import os
import asyncio
import aiofiles as aiof
import aiohttp
import tqdm
from typing import List
import time

# google 搜索的sample url
# https://www.google.com/search?q=%E8%AF%95%E5%8D%B7+filetype%3Adoc

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

url = 'https://www.google.com/search'

proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080',
}

proxy = 'http://127.0.0.1:1080'

# 最多有几个异步函数等待
sem = asyncio.Semaphore(20)


def storePreviewPages(response):
    """
    store the preview pages

    Args:
        response (_type_): _description_
    """
    page_text = response.text
    file_name = type+'.html'
    with open(file_name, 'w', encoding='utf-8') as fp:
        fp.write(page_text)


def extractDocs(response) -> List[str]:
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
            docs.append([a_href, h3_text])
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
        'q': query+' filetype:doc',
        'num': num,
        'start': start
    }
    response = requests.get(url=url, params=param,
                            headers=headers, proxies=proxies)
    docs = extractDocs(response)
    return docs


async def async_download_doc(doc,
                             session: aiohttp.ClientSession,
                             sem: asyncio.Semaphore) -> None:
    doc_url = doc[0]
    doc_path = os.path.join(os.getcwd(), "docs/"+str(doc[1])+".doc")

    # This timeout is useless.
    # timeout = aiohttp.ClientTimeout(total=30)
    # A workaround solution:
    # https://stackoverflow.com/a/64686124
    # https://github.com/aio-libs/aiohttp/issues/3203
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=15)

    async with sem:
        try:
            async with session.get(doc_url, timeout=timeout, proxy=proxy) as response:
                if response.status == 200 and int(response.headers['Content-length']) > 200000:
                    content = await response.read()
                    async with aiof.open(doc_path, "wb") as fhand:
                        await fhand.write(content)
                        await fhand.flush()
                else:
                    print("Unable to download doc {}!".format(doc[1]))
        except Exception as e:
            print(e)


async def downloadDocs(docs, maximum_num_connections: int = 30):
    tasks = []
    sem = asyncio.Semaphore(30)

    connector = aiohttp.TCPConnector(
        limit_per_host=maximum_num_connections, verify_ssl=False)
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


if __name__ == '__main__':
    time_start = time.time()

    docs = query_docIds_on_google("供应链")

    time_end = time.time()

    logTime(time_start, time_end)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(downloadDocs(docs))

    time_end2 = time.time()

    logTime(time_end, time_end2)
