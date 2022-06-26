from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from datetime import *
def getAllPmidsByTerm(term = 'Autism', test=False, incremental=False):
    # 下载一个和chrome版本号一致的chromedriver
    browser = webdriver.Chrome("D:/chromedriver.exe")
    browser.get('https://www.ncbi.nlm.nih.gov/pubmed/?term={0}&dispmax=200'.format(term))
    soup = BeautifulSoup(browser.page_source, "lxml")
    pmids = set()
    page_number = 1
    while True:
        try:
            if page_number == 1:
                if incremental: # 增量的话，就爬取当月初到当月底
                    today = datetime.today()
                    custom_range_link = browser.find_element_by_xpath('//*[@id="facet_date_rangeds1"]')
                    custom_range_link.click()
                    year = today.year
                    month = today.month
                    # start_year
                    browser.find_element_by_xpath('//*[@id="facet_date_st_yeards1"]').send_keys(year)
                    # start_month = browser.find_element_by_xpath('//*[@id="facet_date_st_monthds1"]').send_keys(month)
                    browser.find_element_by_xpath('//*[@id="facet_date_st_monthds1"]').send_keys(month)
                    browser.find_element_by_xpath('//*[@id="facet_date_st_monthds1"]').clear()
                    browser.find_element_by_xpath('//*[@id="facet_date_st_monthds1"]').send_keys(month)
                    # end_year
                    browser.find_element_by_xpath('//*[@id="facet_date_end_yeards1"]').send_keys(year)
                    # end_month
                    browser.find_element_by_xpath('//*[@id="facet_date_end_monthds1"]').send_keys(month)
                    browser.find_element_by_xpath('//*[@id="facet_date_end_monthds1"]').clear()
                    browser.find_element_by_xpath('//*[@id="facet_date_end_monthds1"]').send_keys(month)
                    apply_btn = browser.find_element_by_xpath('//*[@id="facet_date_range_applyds1"]')
                    apply_btn.click()
                link = browser.find_element_by_xpath('//*[@id="EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.Page"]')
            if page_number > 1:
                if bool(browser.find_element_by_xpath('//*[@id="maincontent"]/div/div[3]/div[2]/span[1]')) == True:
                    soup = BeautifulSoup(browser.page_source, "lxml")
                    # 最后一页爬完就返回并退出。
                    for dd in soup.findAll("dd", class_=""):
                        pmid = str(dd).replace("<dd>","").replace("</dd>","")
                        pmids.add(int(pmid))
                    browser.quit()    
                    return pmids
        except NoSuchElementException:
            try:
                link = browser.find_element_by_xpath('(//*[@id="EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.Page"])[3]')
            except NoSuchElementException: # 只有一页，所以没有next按钮也没有其他按钮
                soup = BeautifulSoup(browser.page_source, "lxml")
                for dd in soup.findAll("dd", class_=""):
                    pmid = str(dd).replace("<dd>","").replace("</dd>","")
                    pmids.add(int(pmid))
                return pmids
        except:
            pass 
            break
        soup = BeautifulSoup(browser.page_source, "lxml")
        for dd in soup.findAll("dd", class_=""):
            pmid = str(dd).replace("<dd>","").replace("</dd>","")
            pmids.add(int(pmid))
        try:
            link.click()
            page_number += 1
            if test and page_number > 10:  # debug模式，只插入前200个
                return pmids
        except:
            return pmids
# 测试这个模块
# getAllPmidsByTerm(term = 'Autism', test=False, incremental = True)