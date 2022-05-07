import sqlite
a = sqlite.db('test.db')

a.fill('test/random', 500, True)
data = a.fetch('test/random', timespan=100)
print(data)

a.close()
