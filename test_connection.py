import psycopg2

def test_db():
    conn = psycopg2.connect(
        dbname="support_desk",
        user="postgres",
        password="postgre123",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM customers;")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    test_db()
