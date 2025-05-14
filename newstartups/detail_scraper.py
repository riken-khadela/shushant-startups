from crunch_detail_scraper_summary import SUMMARY
from crunch_detail_scraper_financial import FINANCIAL
from crunch_detail_scraper_news import NEWS
from crunch_detail_scraper_investments import INVESTMENT
import settings as cf
import threading, os


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
        financial = scraper2.financial_process_logic(financialurl)
    
    if investmenturl:
        investment_section=scraper4.investment_process_logic(investmenturl)

    if newsurl:
        news = scraper3.news_process_logic(newsurl)
    
    
    org_detail = {}
    if summary[0] and 'organization_url' in summary[0]:
        org_detail.update(summary[0])
        if financial.get('financial'):
            org_detail.update(financial)
        if investment_section.get('investment'):
            org_detail.update(investment_section)
        if news.get('news'):
            org_detail.update(news)
        
        org_detail["is_updated"] = 1

    return org_detail


def thread_logic():
    dicts = cf.read_crunch_urls(50)
    alldetails = []
    update_urls = []
    threads = []

    def process_and_append(url,dict):
        details = process_organization(url,dict)
        if 'summary' in details:
            alldetails.append(details)

    for dict in dicts:
        url = dict['url']
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
                    cf.insert_organisation_details(alldetails)
                    cf.update_read_stat_urls(update_urls)
                except cf.DuplicateKeyError as e:
                    print("Skipping duplicate records:", e)

            alldetails = []
            update_urls = []
            threads = []

    for thread in threads:
        thread.join()

    alldetails = [details for details in alldetails if 'organization_url' in details]
    if len(alldetails) > 0:
        try:
            cf.insert_organisation_details(alldetails)
            cf.update_read_stat_urls(update_urls)
        except cf.DuplicateKeyError as e:
            print("Skipping duplicate records:", e)


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(file_path, "crunchdetails.txt")
    f = open(filename, 'r')
    txt = f.read()
    f.close()
    if str(txt) == "0":
        f = open(filename, 'w')
        f.write("1")
        f.close()
        try:
            thread_logic()
        except:
            pass
        f = open(filename, 'w')
        f.write("0")
        f.close()
    else:
        print(" Another process is already running")

