from db.connection import connect
from models.stock import Stock
import pandas as pd
import datetime

def get_all_tickers():
    with connect() as conn:
        with conn.cursor() as cur:                
            cur.execute('SELECT DISTINCT ticker FROM public.transac;')
            data =  cur.fetchall()
    return pd.DataFrame(data)

def full_load_history():
    tickers = get_all_tickers()
    data = pd.DataFrame()
    for t in set(tickers[0]):
        st = Stock(t)
        x = st.GetHistoricalQuote()
        data= pd.concat([data, x], ignore_index=True)
    data['loaded_at'] = datetime.datetime.now()
    with connect() as conn:
        with conn.cursor() as cur:  
            cur.execute('TRUNCATE TABLE public.stock_quotes_history')
            print('truncating table public.stock_quotes_history')          
            for _, row in data.iterrows():
                insert_query = """
                                INSERT INTO public.stock_quotes_history(date, open, high, low, close, volume, adjusted_close, ticker, loaded_at)
                                VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s )
                                """
                print(f'Inserting into history data from {row['ticker']} records as of {row['date']}')
                cur.execute(insert_query, (row['date'], row['open'], row['high'], row['low'], row['close'],  row['volume'], row['adjustedClose'], row['ticker'], row['loaded_at']))
            conn.commit()
            print('Full load finished')
            

def incremental_load_history():
    pass
