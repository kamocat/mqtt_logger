import sqlite
import matplotlib.pyplot as plt
a = sqlite.db('test.db')

a.fill('test/random', 500, True)
data = a.fetch('test/random')
plt.plot(data[0], data[1])
plt.show()

a.close()
