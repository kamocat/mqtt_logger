import sqlite3
import time
import math
import datetime

class db:
    def __init__ (self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        try:
            self.cur.execute('''create table topics
                (topic varchar(255))''')
            self.cur.execute('''create table num
                (topic int, value real, start timestamp, end timestamp)''')
            self.con.commit()
        except:
            pass
    def match_topic(self, t):
        # Check if the topic exists
        self.cur.execute("select rowid from topics where topic=:name",{"name":t})
        v = self.cur.fetchone()
        try:
            v = v[0]
        except:
            # Insert the new topic
            self.cur.execute("insert into topics (topic) values (:n)", {"n":t})
            self.con.commit()
            # Get the index
            v = self.cur.lastrowid
        return v

    def insert(self, topic, data, t='now'):
        try:
            data = float(data)
        except:
            print(f"Could not convert to number: {data}")
            return
        n = self.match_topic(topic)
        if( t == 'now' ):
            t = time.time()
        # Check if the value is the same
        self.cur.execute('''select rowid,value from num 
        where topic=:n order by rowid desc''', {'n':n})
        tmp = self.cur.fetchone()
        try:
            prev = {'rowid':tmp[0], 'value':tmp[1], 'end':t}
            assert(math.isclose(prev["value"],data))
            self.cur.execute('''update num set end=:end where
                    rowid=:rowid''',prev)
        except:
            # Add the new value
            self.cur.execute('''insert into num (topic, value, start, end) 
            values (?,?,?,?)''', (n, data, t, t))
        self.con.commit()

    def search(self, topic_text):
        ret = {}
        topic_text += '%' # append wildcard
        query = 'select rowid,topic from topics where topic like :n'
        for row in self.cur.execute(query,{"n":topic_text}):
            ret[row[1]] = row[0]
        return ret

    def fill(self, topic, qty, clear=False):
        if( clear ):
            n = self.match_topic(topic)
            self.cur.execute('delete from num where topic=:n',{'n':n})

        import random as rand
        rand.seed()
        x = 0
        x2 = 0
        t = time.time()
        t = round(t)
        for i in range(qty):
            if(rand.random() > 0.8):
                x += rand.uniform(-0.2,0.5)
            self.insert(topic, math.cos(x), t+i)

    def fetch(self, topic, end_date=None, timespan=60*60*24):
        n = self.match_topic(topic)
        points = []
        if(end_date == None):
            # Get the most recent point
            self.cur.execute('select end from num where topic=:n order by rowid desc limit 1',{'n':n})
            end_date = self.cur.fetchone()[0]
        for row in self.cur.execute('select start,value from num where topic=:n and start<=:s and end>=:e',{'n':n, 's':end_date, 'e':end_date-timespan}):
            x = row[0]
            y = row[1]
            points.append({'time':x, 'value':y})
        return points


    def close(self):
        self.con.close()
