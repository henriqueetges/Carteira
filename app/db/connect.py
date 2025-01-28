from env.config import Config
import psycopg2

configs = Config('production')
DB_USER = configs.get_var('database_user')
DB_PW = configs.get_var('database_pw')
DB_HOST = configs.get_var('database_host')
DB_PORT = configs.get_var('database_port')

def connect():
    params = {
        "dbname": "inv", 
        "user": DB_USER,
        "password": DB_PW,
        "host": DB_HOST,
        "port": DB_PORT,
    }
    try:
        conn = psycopg2.connect(**params)
        return conn

    except (psycopg2.Error, Exception) as e:
        print(e)

print(DB_USER)