from update_crunch_detail_scraper_summary import SUMMARY
from update_crunch_detail_scraper_financial import FINANCIAL
from update_crunch_detail_scraper_news import NEWS 
import update_settings as cf
import threading, os
from datetime import datetime
from update_crunch_detail_scraper_investments import INVESTMENT
from logger import CustomLogger
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = CustomLogger()
number_of_records = 20
number_of_threads = 4
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

import time
def thread_logic():
    
    alldetails = []
    update_urls = []
    dicts = cf.read_crunch_details(number_of_records)
    if not dicts:
        for _ in range(10):
            dicts = cf.read_crunch_details(number_of_records)
            if dicts:
                break
            print("No documents found, sleeping...")
            time.sleep(60)
    

    def process_and_append(url,dict):
        try:
            details = process_organization(url, dict)
            if 'summary' in details:
                return details, dict  
        except Exception as e:
            print(f"[ERROR] Exception in thread: {e}")
            return None, None

    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        future_to_data = {executor.submit(process_and_append, d['organization_url'], d): d for d in dicts}
        
        for future in as_completed(future_to_data):
            try:
                result, update_data = future.result()
                if result and 'organization_url' in result:
                    alldetails.append(result)
                    update_urls.append(update_data)
            except Exception as e:
                print(f"[ERROR] Processing failed: {e}")
                
    alldetails = [details for details in alldetails if 'organization_url' in details]
    if len(alldetails) > 0:
        try:
            cf.update_crunch_detail(alldetails)
        except cf.DuplicateKeyError as e:
            print("Skipping duplicate records:", e)
            
            
# if __name__ == '__main__':
    # file_path = os.path.dirname(os.path.realpath(__file__))
    # filename = os.path.join(file_path, "crunchdetails.txt")
    # print(filename)
    # f = open("/home/user1/startups/shushant-startups/updatestartups/crunchdetails.txt", 'r')
    # txt = f.read()
    # f.close()
    # if str(txt) == "0":
    #     f = open(filename, 'w')
    #     f.write("1")
    #     f.close()
    #     try:
    #         separator_line =  '-' * 40
    #         logger.log(separator_line)
    #         logger.log("            Starting Scraper           ")
    #         logger.log(separator_line)
            
    #         while True :
    #             thread_logic()
                
    #             # if not cf.check_records_updated() :
    #             #     break
    #         logger.log(separator_line)
    #         logger.log("            Stopping Scraper           ")
    #         logger.log(separator_line)
    #     except:
    #         pass
    #     f = open(filename, 'w')
    #     f.write("0")
    #     f.close()
    # else:
    #     logger.warning(" Another process is already running")
    # while True : thread_logic()
    # thread_logic()
# thread_logic()
while True : thread_logic()

