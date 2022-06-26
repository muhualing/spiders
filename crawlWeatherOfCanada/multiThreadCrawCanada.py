import requests
import threading
import os
from tqdm import tqdm
import time

# 用来存放采集线程
g_crawl_list = []
class CrawlThread(threading.Thread):
    def __init__(self, name, page_qeue):
        super(CrawlThread, self).__init__()
        self.name = name
        self.page_queue = page_queue
        self.url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&timeframe=3&submit=Download+Data"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    def run(self):
        print('%s----线程启动' % self.name)
        while 1:
            # 判断采集线程何时退出
            if self.page_queue.empty():
                break
            # 从队列中取出页码
            stationID = self.page_queue.get()
            # 拼接url，发送请求
            url = self.url.format(stationID)
#             print(url)
            r = requests.get(url, headers=self.headers)
            # 响应内容存放到data_queue中
            file = os.path.join(os.getcwd(),"data/"+str(stationID)+".csv")
            fp = open(file, "wb")
            fp.write(r.content)
            fp.close()
#             time.spleep(0.1)
#             with open(file, "wb") as fp:
#                 fp.write(r.content)
        print('%s----线程结束' % self.name)

# 创建队列
def create_queue():
    # 创建页码队列
    page_queue = Queue()
    for stationID in range(100000):
        page_queue.put(stationID)
    # 创建内容队列
    data_queue = Queue()
    return page_queue, data_queue

# 创建采集线程
def create_crawl_thread(page_queue):
    crawl_name = []
    for i in range(5):
        crawl_name.append('采集线程'+str(i))
#     crawl_name = [c + str(i) for c in range()]
#     crawl_name = ['采集线程1', '采集线程2', '采集线程3']
    for name in crawl_name:
        # 创建一个采集线程
        tcrwal = CrawlThread(name, page_queue)
        # 保存到列表中
        g_crawl_list.append(tcrwal)

# 创建队列函数
page_queue, data_queue = create_queue()
# 创建采集线程
create_crawl_thread(page_queue)
# 启动所有采集线程
for tcrwal in g_crawl_list:
    tcrwal.start()
# 主线程等待子线程结束
for tcrwal in g_crawl_list:
    tcrwal.join()
print('主线程子线程全部结束')