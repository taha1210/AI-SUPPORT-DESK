from postgres_tool import run_postgres_query

query = "SELECT * FROM customers;"
result = run_postgres_query(query)

print(result)
