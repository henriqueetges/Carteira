from requests import get
import pandas as pd
from env.config import Config

config = Config('production')
API_KEY = config.get_var('BRAPI_KEY')

class Stock:
    instances = {}
    def __init__(self, ticker):
        self.ticker = ticker
        self.url = f'https://brapi.dev/api/quote/{self.ticker}'
        Stock.instances[self.ticker] = self
    
    @staticmethod
    def GetOrCreate(ticker):
        if ticker in Stock.instances:
            return Stock.instances[ticker]
        return Stock(ticker)

    def GetStockInfo(self):
        params = {
            'modules': 'summaryProfile',
            'token': API_KEY,}
        try:
            req = get(self.url, params=params)
            data = req.json()
            df = pd.DataFrame(data['results'])
            info = pd.json_normalize(df['summaryProfile'])
            return info
        except Exception as e:
            print(e)

    def GetStockQuote(self):
        params = {
            'token': API_KEY}
        try:
            req = get(self.url, params=params)
            data = req.json()
            return pd.DataFrame(data['results'])
        except Exception as e:
            print(e)      

    def GetHistoricalQuote(self):
        params = {
            'token': API_KEY,
            'range':'3mo',
            'interval':'1d',}
        try:
            req = get(self.url, params=params)
            data = req.json()
            results = pd.json_normalize(data,  'results')
            df = pd.DataFrame(results['historicalDataPrice'][0])
            df['date'], df['ticker'] = df['date'].astype('datetime64[s]'), self.ticker
            return df
        except Exception as e:
            print(e)

    def TransformQuotes(data):   
        df = pd.DataFrame(data['results'])
        return df

print(API_KEY)