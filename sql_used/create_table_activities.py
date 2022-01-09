import os
import psycopg2

DATABASE_URL = os.popen(
    'heroku config:get DATABASE_URL -a linebotforkal').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

create_table_query = '''
DROP TABLE IF EXISTS activities;
CREATE TABLE activities(
    id serial PRIMARY KEY,
    userid VARCHAR (50) not null,
    food_name VARCHAR (50),
    kal float,
    unit varchar(50)
);
'''

cursor.execute(create_table_query)
conn.commit()

cursor.close()
conn.close()
