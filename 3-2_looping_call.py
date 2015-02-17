from twisted.internet.task import LoopingCall

class Countdown(object):

    def __init__(self, manager, high, low, dec, delay):
        self.manager = manager
        self.counter = high
        self.low = low
        self.dec = dec
        self.delay = delay
        self.call = LoopingCall(self.count)

    def start(self):
        self.call.start(self.delay)

    def count(self):
        if self.counter < self.low:
            self.call.stop()
            self.manager.end_counter()
        else:
            print self.counter, '...'
            self.counter -= self.dec


class CountdownManager(object):

    def __init__(self):
        self.children = 0

    def spawn(self, high=5, low=0, dec=1, delay=0.5):
        Countdown(self, high, low, dec, delay).start()
        self.children += 1

    def end_counter(self):
        self.children -= 1
        if self.children == 0:
            reactor.stop()
            print "Stop!"


from twisted.internet import reactor

m = CountdownManager()

print 'Start!'
m.spawn()
m.spawn(high=10)
m.spawn(high=20, dec=5)
reactor.run()
