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



def getStockdata(stock):
    data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+stock+'&outputsize=full&apikey=ZCXPM8FMBJXNOE3J&datatype=csv')
    with open('csvFiles/'+stock+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())
        for row in reader:
            writer.writerow(row)

stock = ["AAPL" , "MSFT" , "AMZN" , "FB" , "BRK.B" , "GOOG" , "XOM" , "JPM" , "V" , "BAC" , "INTC" , "CSCO" , "VZ" , "PFE" , "T" , "MA" , "BA" , "DIS" , "KO" , "PEP" , "NFLX" , "MCD" , "WMT" , "ORCL" , "IBM" , "PYPL" , "MMM" , "NVDA" , "NKE" , "COST" , "QCOM" ]

for i in range(len(stock)):
    getStockdata(stock[i]),