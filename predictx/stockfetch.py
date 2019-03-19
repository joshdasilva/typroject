from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
api_key=open('alpha.txt','r').read()
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='60min', outputsize='full')
pprint(data.head(200))
