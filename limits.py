import time
import asyncio
class Alarm:
    def __init__(self, topic, notify, timeout=30):
        self.topic = topic
        self.notify = notify
        self.limits = []
        self.interval = timeout * 60 #max seconds between messages
        self.alive = True
        self.feed()
    def feed(self):
        self.expire = time.monotonic() + self.interval
        self.alive = True
    def watchdog(self):
        if time.monotonic() > self.expire and self.alive:
            self.alive = False
            self.send_alert(f'{self.topic} stopped responding')
    def limit(self, test, msg):
        try: test(0)
        except: print(f'Warning: Test {test} does not accept numeric data')
        self.limits.append({'test':test, 'msg':msg, 'state':False})
    def send_alert(self, msg):
        print(f'Sent alert to {self.notify}: {msg}')
        #TODO: Send actual email
    def test(self, topic, value):
        if topic == self.topic:
            self.feed()
            try: value = float(value)
            except: 
                print(f'Warning: {value} is not numeric')
                return
            for limit in self.limits:
                new_state = limit['test'](value)
                if new_state and not limit['state']:
                    self.send_alert(limit['msg'])
                limit['state'] = new_state
           

async def watchdog(topics):
    while(1):
        for topic in topics:
            topic.watchdog()
        await asyncio.sleep(5)

marshal = 'kamocat@gmail.com'

limits = []

test = Alarm(topic='/test', notify=[marshal], timeout=1)
test.limit(test=(lambda x: x>3), msg='Test value is too high')
test.limit(test=(lambda x: x<=0), msg='Test value is too low')


limits.append(test)
