import sqlite
a = sqlite.db('waterwall.db')

a.fill('test/random1', 100)
a.fill('test/random2', 200)
a.fill('test/random3', 500)
a.fill('test/random4', 1000)
a.close()
