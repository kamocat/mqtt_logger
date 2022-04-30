import sqlite3
con = sqlite3.connect("test.db")
cur = con.cursor()
try:
    cur.execute('''create table topics
            (id int not null primary key, topic varchar(255))''')
    cur.execute('''create table num
            (id int not null primary key, topic int, value real, start timestamp, 
            end timestamp)''')
    con.commit()
except:
    print("tables already created")

def match_topic(t):
    cur.execute(f"select * from topics where topic=:name",{"name":t})
    print(cur.fetchone())
    

match_topic("test/setpoint")
match_topic("invalid")


con.close()
