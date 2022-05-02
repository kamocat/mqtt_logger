import sqlite3
import time
import math

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

    def insert(self, topic, data):
        try:
            data = float(data)
        except:
            print(f"Could not convert to number: {data}")
            return
        n = self.match_topic(topic)
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


    def close(self):
        self.con.close()


# Test code
if __name__ == '__main__':
    a = db('test.db')
    #print(a.match_topic("test/one"))
    a.insert('test/two', '35.3')
    a.close()
