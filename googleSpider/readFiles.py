import os
import asyncio
import aiofiles as aiof
import aiohttp
import tqdm
import random

file_path = os.path.join(os.getcwd(),"urls1.txt")
file = open(file_path, 'r', encoding='utf-8')
Lines = file.readlines()

count = 0
queries = []
for line in Lines:
    count += 1
    queries.append(line.split('\t'))

fileWriteCount = 0

async def async_download_doc(doc,
                             session: aiohttp.ClientSession,
                             sem: asyncio.Semaphore) -> None:
    doc_url = doc[0]
    doc[2] = doc[2].strip('\n')
    if doc[1] == '':
        doc[1] = str(random.randint(0, 9)) + doc[2]
    doc_path = os.path.join(os.getcwd(), 'docs1', doc[2], str(doc[1])+".doc")
    if doc_url.endswith('.docx'):
        doc_path = os.path.join(os.getcwd(), 'docs1', doc[2], str(doc[1])+".docx")
    global fileWriteCount
    if os.path.exists(doc_path):
        fileWriteCount += 1
        print("File write count: {}".format(fileWriteCount))
        return

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
                if int(response.headers['Content-length']) < 50000:
                    return
                #     print("File is too small" + ": {}".format(response.headers['Content-length']))
                dir_path = os.path.join(os.getcwd(), 'docs1', doc[2])
                isExist = os.path.exists(dir_path)
                if not isExist:
                    # Create a new directory because it does not exist 
                    os.makedirs(dir_path)
                content = await response.read()
                try:
                    async with aiof.open(doc_path, "wb") as fhand:
                        await fhand.write(content)
                        await fhand.flush()
                        fileWriteCount += 1
                        print("File {} written!".format(doc[1]))
                        print("File write count: {}".format(fileWriteCount))
                except Exception as e:
                    doc[1] = str(random.randint(0, 9)) + doc[2]
                    doc_path = os.path.join(os.getcwd(), 'docs1', doc[2], str(doc[1])+".doc")
                    async with aiof.open(doc_path, "wb") as fhand:
                        await fhand.write(content)
                        await fhand.flush()
                        fileWriteCount += 1
                        print("File write count: {}".format(fileWriteCount))
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

loop = asyncio.get_event_loop()
loop.run_until_complete(downloadDocs(queries))