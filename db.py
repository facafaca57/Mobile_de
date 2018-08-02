import sqlite3
 
conn = sqlite3.connect("cars.db") 
cursor = conn.cursor()
try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS cars_car
                    (id integer primary key autoincrement, title text, descriptions text, producer text, model text, year text, price text, img text)
                """)
except:
    print("Така таблиця вже їснує..")