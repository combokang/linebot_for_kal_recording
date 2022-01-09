import os
import psycopg2

DATABASE_URL = os.popen("heroku config:get DATABASE_URL -a linebotforkal").read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

create_table_query = """
DROP TABLE IF EXISTS userinfo;
CREATE TABLE userinfo(
    userID VARCHAR (50) PRIMARY KEY,
    TDEE float,
    today_kal_left float,
    status varchar(10),
    gender varchar(10),
    high float,
    weight float,
    age int,
    activity varchar(10)
);
"""

print("更新完成")

cursor.execute(create_table_query)
conn.commit()

cursor.close()
conn.close()
