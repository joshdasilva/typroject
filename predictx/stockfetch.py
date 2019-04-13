# from alpha_vantage.timeseries import TimeSeries
# import csv
# import io
# import pandas as pd
# from pprint import pprint
#
# api_key=open('alpha.txt','r').read()
# ts = TimeSeries(key=api_key, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='MSFT',interval='60min', outputsize='full')
# pprint(data.columns)
# #df = pd.read_csv(io.StringIO(data.))
# #print(df.head())
# #df.to_csv('out.csv')
#
import csv
import requests
from bs4 import BeautifulSoup


#
# def getStockdata(stock):
#     data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+stock+'&outputsize=full&apikey=ZCXPM8FMBJXNOE3J&datatype=csv')
#     with open('csvFiles/'+stock+'.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         reader = csv.reader(data.text.splitlines())
#         for row in reader:
#             writer.writerow(row)
#
# stock = ["AAPL" , "MSFT" , "AMZN" , "FB" , "BRK.B" , "GOOG" , "XOM" , "JPM" , "V" , "BAC" , "INTC" , "CSCO" , "VZ" , "PFE" , "T" , "MA" , "BA" , "DIS" , "KO" , "PEP" , "NFLX" , "MCD" , "WMT" , "ORCL" , "IBM" , "PYPL" , "MMM" , "NVDA" , "NKE" , "COST" , "QCOM" ]
#
# for i in range(len(stock)):
#     getStockdata(stock[i]),


def scrape_all_articles(ticker, upper_page_limit=5):
    landing_site = 'http://www.nasdaq.com/symbol/' + ticker + '/news-headlines'
    all_news_urls = get_news_urls(landing_site)
    current_urls_list = all_news_urls.copy()
    index = 2

    '''Loop through each sequential page, scraping the links from each'''
    while (current_urls_list is not None) and (current_urls_list != []) and \
            (index <= upper_page_limit):
        '''Construct URL for page in loop based off index'''
        current_site = landing_site + '?page=' + str(index)
        current_urls_list = get_news_urls(current_site)
        '''Append current webpage's list of urls to all_news_urls'''
        all_news_urls = all_news_urls + current_urls_list
        index = index + 1

    all_news_urls = list(set(all_news_urls))
    '''Now, we have a list of urls, we need to actually scrape the text'''
    all_articles = [scrape_news_text(news_url) for news_url in all_news_urls]
    return all_articles

def get_news_urls(links_site):
    '''scrape the html of the site'''
    resp = requests.get(links_site)

    if not resp.ok:
        return None

    html = resp.content
    '''convert html to BeautifulSoup object'''
    soup = BeautifulSoup(html, 'lxml')
    '''get list of all links on webpage'''
    links = soup.find_all('a')
    urls = [link.get('href') for link in links]
    urls = [url for url in urls if url is not None]
    '''Filter the list of urls to just the news articles'''
    news_urls = [url for url in urls if '/article/' in url]
    return news_urls

def scrape_news_text(news_url):
    news_html = requests.get(news_url).content
    '''convert html to BeautifulSoup object'''
    news_soup = BeautifulSoup(news_html, 'lxml')
    paragraphs = [par.text for par in news_soup.find_all('p')]
    news_text = '\n'.join(paragraphs)
    return news_text





nflx_articles = scrape_all_articles('mmm', 5)
print(nflx_articles[0])