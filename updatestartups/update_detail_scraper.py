from update_crunch_detail_scraper_summary import SUMMARY
from update_crunch_detail_scraper_financial import FINANCIAL
from update_crunch_detail_scraper_news import NEWS 
import update_settings as cf
import threading, os
from datetime import datetime
from update_crunch_detail_scraper_investments import INVESTMENT
from logger import CustomLogger

logger = CustomLogger()

def process_organization(url,dict):
    scraper = SUMMARY()
    scraper2 = FINANCIAL()
    scraper3 = NEWS()
    scraper4=INVESTMENT()
    summary = scraper.summary_process_logic(url,dict)
    financialurl = summary[1]
    newsurl = summary[2]
    investmenturl=summary[3]
    financial = {}
    news = {}
    investment_section={}

    if financialurl:
        financial = scraper2.financial_process_logic(financialurl,dict)
    
    if investmenturl:
        investment_section=scraper4.investment_process_logic(investmenturl,dict)

    if newsurl:
        news = scraper3.news_process_logic(newsurl,dict)
    
    org_detail = {}
    if summary[0] and 'organization_url' in summary[0]:
        org_detail.update(summary[0])
        org_detail["is_updated"] = 1
        org_detail["update_timestamp"]=datetime.now()
        if financial.get('financial'):
            org_detail.update(financial)
        if investment_section.get('investment'):
            org_detail.update(investment_section)
        if news.get('news'):
            org_detail.update(news)

    return org_detail


def thread_logic():
    dicts = cf.read_crunch_details(20)
   
    alldetails = []
    update_urls = []
    threads = []

    def process_and_append(url,dict):
        details = process_organization(url,dict)
        if 'summary' in details:
            alldetails.append(details)

    for dict in dicts:
        url = dict['organization_url']
        thread = threading.Thread(target=process_and_append, args=(url,dict))
        threads.append(thread)
        thread.start()

        update_urls.append(dict)

        if len(threads) >= 10:
            for thread in threads:
                thread.join()

            alldetails = [details for details in alldetails if 'organization_url' in details]
            if len(alldetails) > 0:
                try:
                    cf.update_crunch_detail(alldetails)
                except cf.DuplicateKeyError as e:
                    logger.log("Skipping duplicate records:", e)

            alldetails = []
            update_urls = []
            threads = []

    for thread in threads:
        thread.join()

    alldetails = [details for details in alldetails if 'organization_url' in details]
    if len(alldetails) > 0:
        try:
            cf.update_crunch_detail(alldetails)
        except cf.DuplicateKeyError as e:
            logger.log("Skipping duplicate records:", e)

if __name__ == '__main__':
    file_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(file_path, "crunchdetails.txt")
    print(filename)
    f = open(filename, 'r')
    txt = f.read()
    f.close()
    if str(txt) == "0":
        f = open(filename, 'w')
        f.write("1")
        f.close()
        try:
            separator_line =  '-' * 40
            logger.log(separator_line)
            logger.log("            Starting Scraper           ")
            logger.log(separator_line)
            thread_logic()
            logger.log(separator_line)
            logger.log("            Stopping Scraper           ")
            logger.log(separator_line)
        except:
            pass
        f = open(filename, 'w')
        f.write("0")
        f.close()
    else:
        logger.warning(" Another process is already running")

#thread_logic()

