from os import getenv
from dotenv import load_dotenv
from supabase import create_client

class Connection:
    def __init__(self, url, key):
        self.conn = create_client(url, key)
    
    def get_connection(self):
        return self.conn
    
    def close(self):
        self.conn = None
        

if __name__ == "__main__":
    load_dotenv()
    url = getenv("SUPABASE_URL")
    key = getenv("SUPABASE_KEY")
    try:
        connection = Connection(url, key)
        conn = connection.get_connection()
        print(conn)
        print("Connection is successful")
    except Exception as e:
        print("connection is failed")
    finally:
        connection.close()
        print("Connection is clossed")
        