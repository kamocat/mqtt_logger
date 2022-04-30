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

    def insert(self, topic, data):
        try:
            data = float(data)
        except:
            print(f"Could not convert to number: {data}")
            return
        t = time.time()
        # Check if the value is the same
        self.cur.execute('''select rowid,value from num 
        where topic=:n order by rowid desc''', {'n':topic})
        tmp = self.cur.fetchone()
        try:
            prev = {'rowid':tmp[0], 'value':tmp[1], 'end':t}
            assert(math.isclose(prev["value"],data))
            self.cur.execute('''update num set end=:end where
                    rowid=:rowid''',prev)
        except:
            # Add the new value
            self.cur.execute('''insert into num (topic, value, start, end) 
            values (?,?,?,?)''', (topic, data, t, t))
        self.con.commit()


    def close(self):
        self.con.close()


# Test code
if __name__ == '__main__':
    a = db('test.db')
    a.insert('test/two', '35.3')
    a.close()
