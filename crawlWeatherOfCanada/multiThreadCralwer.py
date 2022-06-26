import threading
import time
from queue import Queue
import requests
import os

# 用来存放采集线程
g_crawl_list = []
# 用来存放解析线程
g_parse_list = []

class CrawlThread(threading.Thread):
    def __init__(self, name, page_queue, data_queue):
        super(CrawlThread, self).__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=\
        {}&timeframe=3&submit=Download+Data"
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
            r = requests.get(url, headers=self.headers)
            # 响应内容存放到data_queue中
            self.data_queue.put((stationID, r.content))
        print('%s----线程结束' % self.name)

class ParserThread(threading.Thread):
    def __init__(self, name, data_queue):
        super(ParserThread, self).__init__()
        self.name = name
        self.data_queue = data_queue

    def run(self):
        print('%s----线程启动' % self.name)
        while 1:
            try:
                # 从data_queue中取出一页数据
                data = self.data_queue.get(True, 10)
                stationID, content = data
                file = os.getcwd()+'/data2/'+ str(stationID) + ".csv"
                fp = open(file, "wb")
                fp.write(content)
                fp.close()
            except Exception as e:
                break
        print('%s----线程结束' % self.name)

# 创建队列
def create_queue():
    # 创建页码队列
    page_queue = Queue()
    for stationID in range(10000):
        page_queue.put(stationID)
    # 创建内容队列
    data_queue = Queue()
    return page_queue, data_queue

# 创建采集线程
def create_crawl_thread(page_queue, data_queue):
    crawl_name = ['采集线程1', '采集线程2', '采集线程3']
    for name in crawl_name:
        # 创建一个采集线程
        tcrwal = CrawlThread(name, page_queue, data_queue)
        # 保存到列表中
        g_crawl_list.append(tcrwal)

# 创建解析线程
def create_parse_thread(data_queue):
    parse_name = ['解析线程1', '解析线程2', '解析线程3']
    for name in parse_name:
        # 创建一个解析线程
        tparse = ParserThread(name, data_queue)
        # 保存到列表中
        g_parse_list.append(tparse)

def main():
    # 创建队列函数
    page_queue, data_queue = create_queue()
    # 创建采集线程
    create_crawl_thread(page_queue, data_queue)
    # 创建解析线程
    create_parse_thread(data_queue)
    # 启动所有采集线程
    for tcrwal in g_crawl_list:
        tcrwal.start()
    # 启动所有解析线程
    for tparse in g_parse_list:
        tparse.start()
    # 主线程等待子线程结束
    for tcrwal in g_crawl_list:
        tcrwal.join()
    for tparse in g_parse_list:
        tparse.join()
    print('主线程子线程全部结束')

if __name__ == '__main__':
    main() 
    print(5)