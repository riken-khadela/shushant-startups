from crunch_detail_scraper_summary import SUMMARY
from crunch_detail_scraper_financial import FINANCIAL
from crunch_detail_scraper_news import NEWS
from crunch_detail_scraper_investments import INVESTMENT
import settings as cf
import threading, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

threads_num = 4
number_of_records = 100

def process_organization(url,dict):
    org_detail = {}
    try :
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
            financial = scraper2.financial_process_logic(financialurl)
        
        if investmenturl:
            investment_section=scraper4.investment_process_logic(investmenturl)

        if newsurl:
            news = scraper3.news_process_logic(newsurl)
        
        if summary[0] and 'organization_url' in summary[0]:
            org_detail.update(summary[0])
            if financial.get('financial'):
                org_detail.update(financial)
            if investment_section.get('investment'):
                org_detail.update(investment_section)
            if news.get('news'):
                org_detail.update(news)
            
            org_detail["is_updated"] = 1
    except Exception as e:
        print(e)
        
    return org_detail


def thread_logic():
    alldetails = []
    update_urls = []
    dicts = cf.read_crunch_urls(number_of_records)
    if not dicts:
        for _ in range(10):
            dicts = cf.read_crunch_urls(number_of_records)
            if dicts:
                break
            print("No documents found, sleeping...")
            time.sleep(60)
            
    def process_and_append(url,dict):
        try:
            result = process_organization(url, dict)
            if 'summary' in result:
                return result, dict  
        except Exception as e:
            print(f"[ERROR] Exception in thread: {e}")
            return None, None
            
    with ThreadPoolExecutor(max_workers=threads_num) as executor:
        future_to_data = {executor.submit(process_and_append, d['url'], d): d for d in dicts}
        
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
            cf.insert_organisation_details(alldetails)
            cf.update_read_stat_urls(update_urls)
        except cf.DuplicateKeyError as e:
            print("Skipping duplicate records:", e)

# if __name__ == '__main__':
#     file_path = os.path.dirname(os.path.realpath(__file__))
#     filename = os.path.join(file_path, "crunchdetails.txt")
#     f = open(filename, 'r')
#     txt = f.read()
#     f.close()
#     if str(txt) == "0":
#         f = open(filename, 'w')
#         f.write("1")
#         f.close()
#         try:
#             thread_logic()
#         except:
#             pass
#         f = open(filename, 'w')
#         f.write("0")
#         f.close()
#     else:
#         print(" Another process is already running")

