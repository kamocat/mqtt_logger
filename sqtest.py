import sqlite
a = sqlite.db('waterwall.db')

a.fill('test/random1', 1000)
a.fill('test/random2', 2000)
a.fill('test/random3', 1500)
a.fill('test/random4', 1000)
a.close()
