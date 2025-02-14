import psycopg2
import config  # Import the whole module instead of specific names

def connect_to_db():
    try:
        connection = psycopg2.connect(
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT
        )
        print("Database connection successful!")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

if __name__ == "__main__":
    connect_to_db()