from db import connect
from models.stock import Stock
import datetime
import pandas as pd


class Transacao:
    instances = []
    def __init__(self, ticker: str, preco: float, quantidade: int, data: datetime.date = None):
        self.ticker = ticker
        self.price = preco
        self.quantity = quantidade
        self.date = data if data else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Transacao.instances.append(self)
        self.stock = Stock.GetOrCreate(self.ticker)
        try:
            self.insert_into_db()
        except Exception as e:
            print(f"Error inserting transaction: {e}")

    def __repr__(self):
        return f"Transacao do {self.ticker} ao preço de {self.price} e {self.quantity} unidades, feita na data de'{self.date}'"


    def insert_into_db(self):
        with connect() as conn:
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO inv.public.transac(ticker, price, quantity, transac_date)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (self.ticker, self.price, self.quantity, self.date))
                conn.commit()
                
    @classmethod
    def get_from_backend(cls):
        cls.instances.clear()
        conn = connect()
        results = pd.read_sql_query("SELECT * FROM inv.public.transac", conn)
        for _, row in results.iterrows():
            Transacao(ticker=row['ticker'], 
                preco=row['price'],
                quantidade=row['quantity'],
                data=row['transac_date'])
        return Transacao.instances