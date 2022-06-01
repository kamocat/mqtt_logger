import time
import asyncio
import mailjet
import typing
class Alarm:
    def __init__(self, topic:str, notify:list[str], timeout:float=30):
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
    def limit(self, limit_pass:float, limit_fail:float, msg:str):
        self.limits.append({'lpass':limit_pass, 'lfail':limit_fail, 'state':False, 'msg':msg})
    def send_alert(self, msg):
        #mailjet.send(msg, self.notify)
        print(f'Sent email to {self.notify}: {msg}')
    def test(self, topic:str, value):
        if topic == self.topic:
            self.feed()
            try: value = float(value)
            except: 
                print(f'Warning: {value} is not numeric')
                return
            for limit in self.limits:
                flip = limit['lpass']>limit['lfail']
                lfail = (limit['lfail'] < value) != flip
                lpass = (limit['lpass'] > value) != flip
                if lfail and not limit['state']:
                    self.send_alert(limit['msg'])
                    limit['state'] = True
                elif lpass and limit['state']:
                    limit['state'] = False
           

async def watchdog(topics):
    while(1):
        for topic in topics:
            topic.watchdog()
        await asyncio.sleep(5)

marshal = "mhece.api@gmail.com"

limits = []

test = Alarm(topic='/test', notify=[marshal], timeout=1)
test.limit(limit_pass = 3.5, limit_fail = 4.1, msg='Test value is too high')
test.limit(limit_pass = 1, limit_fail = 0, msg='Test value is too low')


limits.append(test)
