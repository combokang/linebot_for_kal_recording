import os
import psycopg2

DATABASE_URL = os.popen(
    'heroku config:get DATABASE_URL -a linebotforkal').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

insert_query = '''
DELETE from Food_Calories where food_name = '蘋果';
DELETE from userinfo where userid = 'U564a432faeb8b9f402b67152dc8a13ad';
DELETE from activities where userid = 'U564a432faeb8b9f402b67152dc8a13ad';
INSERT into Food_Calories(food_name,unit,kal,select_time) VALUES('蘋果','顆','50',0);
INSERT into userinfo(userid,TDEE,today_kal_left) VALUES('U564a432faeb8b9f402b67152dc8a13ad',500,500);
INSERT into activities(userid) VALUES('U564a432faeb8b9f402b67152dc8a13ad');'''

cursor.execute(insert_query)
conn.commit()
cursor.close()

cursor = conn.cursor()
select_query_1 = '''select * from Food_Calories'''
cursor.execute(select_query_1)
print(cursor.fetchone())

cursor = conn.cursor()
select_query_2 = '''select * from userinfo'''
cursor.execute(select_query_2)
print(cursor.fetchone())
cursor.close()

conn.close()
