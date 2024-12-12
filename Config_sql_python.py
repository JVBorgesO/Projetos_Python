#import pyodbc
#import pandas as pd

server = ''
database = ''
username = ''
password = ''

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def simpleQuery(query):
    try:
        conn = pyodbc.connect(conn_str)
        
        data = pd.read_sql(query, conn)
        
        conn.close()

        return pd.DataFrame(data)
    except Exception as e:
        print(f'Error: {e}')
