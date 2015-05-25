class CurrentStep(object):
    def __init__(self,iterator):
        self.it = iterator
        self.cnt = 0
        self.curr = None
        try:
           self._next = self.it.next
        except AttributeError:
           self._next = self.it.__next__
        self.curr = self._next()

    def step(self):
        self.curr = self._next()
        self.cnt +=1

    def current(self):
        return self.curr

