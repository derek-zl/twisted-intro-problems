from twisted.internet.task import LoopingCall

class Countdown(object):

    def __init__(self, manager, high, low, dec, delay):
        self.manager = manager
        self.counter = high
        self.low = low
        self.dec = dec
        self.delay = delay

    def count(self):
        if self.counter == self.low:
            self.manager.end_counter()
        else:
            print self.counter, '...'
            self.counter -= self.dec

class CountdownManager(object):

    def __init__(self):
        self.children = 0

    def start(self):
        for counter in self.children:
            counter.start()


    def spawn(self, high=5, low=0, dec=1, delay=1):
        counter = reactor.LoopingCall(Countdown(self, high, low, dec, delay).count)
        self.children += 1

    def end_counter(self):
        self.children -= 1
        if len(self.children) == 0:
            reactor.stop()


from twisted.internet import reactor

m = CountdownManager()
m.spawn()
m.spawn(high=10)
m.spawn(high=20, dec=5)

print 'Start!'
reactor.run()
print 'Stop!'
