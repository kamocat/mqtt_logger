class Alarm:
    def __init__(self, topic, notify):
        self.topic = topic
        self.notify = notify
        self.limits = []
    def limit(self, test, msg):
        try: test(0)
        except: print(f'Warning: Test {test} does not accept numeric data')
        self.limits.append({'test':test, 'msg':msg, 'state':False})
    def send_alert(self, msg):
        print(f'Sent alert to {self.notify}: {msg}')
        #TODO: Send actual email
    def test(self, topic, value):
        if topic == self.topic:
            try: value = float(value)
            except: 
                print(f'Warning: {value} is not numeric')
                return
            for limit in self.limits:
                new_state = limit['test'](value)
                if new_state and not limit['state']:
                    self.send_alert(limit['msg'])
                limit['state'] = new_state
           



marshal = 'kamocat@gmail.com'

limits = []

test = Alarm(topic='/test', notify=[marshal])
test.limit(test=(lambda x: x>3), msg='Test value is too high')
test.limit(test=(lambda x: x<=0), msg='Test value is too low')


limits.append(test)
