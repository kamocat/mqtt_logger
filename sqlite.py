import aiosqlite
import time
import math
import datetime

class db:
    async def __init__ (self, path):
        self.con = await aiosqlite.connect(path)
        self.cur = await self.con.cursor()
        try:
            await self.cur.execute('''create table topics
                (id integer primary key asc, topic varchar(255))''')
            await self.cur.execute('''create table num
                (topic int, value real, start timestamp, end timestamp)''')
            await self.con.commit()
        except:
            pass

    async def fetch_topic(self, t):
        # Check if the topic exists
        await self.cur.execute("select id from topics where topic=:name",{"name":t})
        v = await self.cur.fetchone()
        try:
            v = v[0]
        except:
            v = -1
        return v

    async def insert_topic(self, t):
        n = await self.fetch_topic(topic)
        if n<1:
            # Insert the new topic
            await self.cur.execute("insert into topics (topic) values (:n)", {"n":t})
            await self.con.commit()
            # Get the index
            n = await self.cur.lastrowid
        return n

    async def insert(self, topic, data, t='now'):
        try:
            data = float(data)
        except:
            print(f"Could not convert to number: {data}")
            return
        if( t == 'now' ):
            t = time.time()
        # Check if the value is the same
        n = await self.cur.insert_topic(topic)
        await self.cur.execute('''select rowid,value from num 
        where topic=:n order by rowid desc''', {'n':n})
        tmp = await self.cur.fetchone()
        try:
            prev = {'rowid':tmp[0], 'value':tmp[1], 'end':t}
            assert(math.isclose(prev["value"],data))
            await self.cur.execute('''update num set end=:end where
                    rowid=:rowid''',prev)
        except:
            # Add the new value
            await self.cur.execute('''insert into num (topic, value, start, end) 
            values (?,?,?,?)''', (n, data, t, t))
        await self.con.commit()

    async def search(self, topic_text):
        ret = {}
        topic_text += '%' # append wildcard
        query = 'select id,topic from topics where topic like :n'
        async for row in self.cur.execute(query,{"n":topic_text}):
            ret[row[1]] = row[0]
        return ret

    async def fill(self, topic, qty, clear=False):
        if( clear ):
            n = self.insert_topic(topic)
            await self.cur.execute('delete from num where topic=:n',{'n':n})

        import random as rand
        rand.seed()
        x = 0
        x2 = 0
        t = time.time()
        t = round(t)
        offset = rand.uniform(-5,5)
        for i in range(qty):
            if(rand.random() > 0.8):
                x += rand.uniform(-0.2,0.5)
            await self.insert(topic, offset+math.cos(x), t+i*300)

    async def fetch(self, topic, end_date=None, days=1):
        timespan = days * 60*60*24
        n = await self.fetch_topic(topic)
        x = []
        y = []
        if(end_date == None):
            # Get the most recent point
            await self.cur.execute('select end from num where topic=:n order by rowid desc limit 1',{'n':n})
            end_date = await self.cur.fetchone()[0]
        async for row in self.cur.execute('select start,value,end from num where topic=:n and start<=:s and end>=:e',{'n':n, 's':end_date, 'e':end_date-timespan}):
            x.append(row[0])
            y.append(row[1])
            if(row[2] != row[0]): #Show the duration of the point
                x.append(row[2])
                y.append(row[1])
        return {"time":x, "value":y}

    async def latest(self, topic):
        n = await self.fetch_topic(topic)
        await self.cur.execute('select start,end,value from num where topic=:n order by rowid desc limit 1',{'n':n})
        res = await self.cur.fetchone()
        return {'start':res[0], 'end':res[1], 'value':res[2]}
        
    async def close(self):
        await self.con.close()
