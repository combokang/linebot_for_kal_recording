import os
import psycopg2

DATABASE_URL = os.popen(
    'heroku config:get DATABASE_URL -a linebotforkal').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

create_table_query = '''
DROP TABLE IF EXISTS Food_Calories;
CREATE TABLE Food_Calories(
    foodID serial PRIMARY KEY,
    food_name VARCHAR (50) NOT NULL,
    unit VARCHAR (50) NOT NULL,
    kal float NOT NULL,
    select_time Int
);
'''

cursor.execute(create_table_query)
conn.commit()

cursor.close()
conn.close()
