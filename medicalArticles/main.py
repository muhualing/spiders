from crawler import crawl
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
if __name__ == '__main__':
    # 第一次全量爬取
    crawl()
    # 间隔一天运行一次增量爬取
    scheduler = BlockingScheduler()
    scheduler.add_job(crawl(incremental=True), 'interval', days=1)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass