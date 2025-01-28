from env.config import Config
from models.stock import Stock
from models.transaction import Transacao
from db.connect import connect



with connect() as conn:
    with conn.cursor() as cur:
        query = """
                SELECT version();

                """ 
        cur.execute(query)
        version = cur.fetchone()

            
            
print(version)