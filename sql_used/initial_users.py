import os
import psycopg2

DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a linebotforkal").read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

insert_query = """
DELETE from userinfo where userid = 'Uef187c8e0efdacea7bdcd0f221ac4599';
DELETE from activities where userid = 'Uef187c8e0efdacea7bdcd0f221ac4599';"""

cursor.execute(insert_query)
conn.commit()
cursor.close()

cursor = conn.cursor()
select_query_1 = """select * from activities"""
cursor.execute(select_query_1)
print(cursor.fetchone())

cursor = conn.cursor()
select_query_2 = """select * from userinfo"""
cursor.execute(select_query_2)
print(cursor.fetchone())
cursor.close()

conn.close()
