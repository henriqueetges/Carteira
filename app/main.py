from db.connection import connect
from models.stock import Stock
from models.transaction import Transacao

with connect() as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT VERSION();')
        version = cur.fetchone()

print(version)