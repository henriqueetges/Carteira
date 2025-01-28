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