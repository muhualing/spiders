import pymysql

conn = pymysql.connect(
    host="40.81.21.206",
    port=8788,
    user="root",
    password="root",
    database="docs",
    charset="utf8"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM docs")

results = cursor.fetchall()