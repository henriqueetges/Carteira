from env.config import configs
import psycopg2



def connect():
    params = {
        "dbname": "inv", 
        "user": configs.DB_USER,
        "password": configs.DB_PW,
        "host": configs.DB_HOST,
        "port": configs.DB_PORT,
    }
    try:
        conn = psycopg2.connect(**params)
        return conn

    except (psycopg2.Error, Exception) as e:
        print(e)
