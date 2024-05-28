import sqlite3

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()


def display_first_20_rows(table_name):
    print(f"Первые 20 строк таблицы {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 20")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()


display_first_20_rows("city")
display_first_20_rows("weather")

conn.close()
