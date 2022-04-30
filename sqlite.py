import sqlite3
import types
con = sqlite3.connect("test.db")
cur = con.cursor()
try:
    cur.execute('''create table topics
            (topic varchar(255))''')
    cur.execute('''create table num
            (topic int, value real, start timestamp, end timestamp)''')
    con.commit()
except:
    print("tables already created")

def match_topic(t)
    # Check if the topic exists
    cur.execute("select rowid from topics where topic=:name",{"name":t})
    v = cur.fetchone()
    try:
        v = v[0]
    except:
        # Insert the new topic
        cur.execute("insert into topics (topic) values (:n)", {"n":t})
        con.commit()
        # Get the index
        cur.execute("select rowid from topics order by rowid desc")
        v = cur.fetchone()
        v = v[0]
    return v
    

match_topic("test/setpoint")
match_topic("invalid")


con.close()
