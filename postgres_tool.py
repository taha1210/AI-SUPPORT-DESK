import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def run_postgres_query(query: str):
    """
    Execute a SQL query on PostgreSQL and return results
    """
    try:
        if not query.strip().lower().startswith("select"):
            return {"error": "Only SELECT queries are allowed"}

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    except Exception as e:
        return {"error": str(e)}
