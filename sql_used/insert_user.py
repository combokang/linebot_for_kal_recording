import os
import psycopg2

DATABASE_URL = os.popen(
    'heroku config:get DATABASE_URL -a linebotforkal').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

insert_query = '''

INSERT into userinfo(userid,TDEE,today_kal_left) VALUES('Uad942c926a2b4dda631261116ff8cdf3',500,500);
INSERT into activities(userid) VALUES('Uad942c926a2b4dda631261116ff8cdf3');'''

cursor.execute(insert_query)
conn.commit()
cursor.close()

cursor = conn.cursor()
select_query_2 = '''select * from userinfo'''
cursor.execute(select_query_2)
result = cursor.fetchall()
for i in result:
    print(i)
cursor.close()

conn.close()
