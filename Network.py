import numpy as np
from functools import wraps
import inspect

def initializer(func):
    """
    Automatically assigns the parameters.

    >>> class process:
    ...     @initializer
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    names, varargs, keywords, defaults = inspect.getargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kargs):
        for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)

        for name, default in zip(reversed(names), reversed(defaults)):
            if not hasattr(self, name):
                setattr(self, name, default)

        func(self, *args, **kargs)

    return wrapper


class Network(object):
    @initializer
    def __init__(self,
    num_source = 5,
    num_server = 1,
    num_packet = 1000,
    arrival = ("poisson",[1]*5),
    service = ("exponential",[0.1]*5),
    queue = "FCFS",
    preemption = False,
    scheduler = "MAF"):

        self.generator = self.Packet_Generator(num_packet,num_source,arrival)
        self.queue = self.Queue(queue)
        self.scheduler = self.

    def generateSampleTimes(self,num_packet = 1000, type = "poisson", rate="default"):
        if rate == "default":
            rate = [1]*self.num_source

        self.num_packet = num_packet

        if type == "poisson":
            self.arr_TS = np.random.exponential(rate,(num_packet,self.num_source))
        elif type == "deterministic":
            self.arr_TS = np.ones(num_packet,self.num_source)*1

        self.arr_TS = np.cumsum(self.arr_TS,0)

    class Queue(object):
        def __init__(self):
            return
        def in(self):
            return
        def out(self):
            return

    class Packet_Generator(object):
        def __init__(self,num_packet,num_source,arrival,seed = 0):
            if arrival[0] == "poisson":
                self.arr = np.random.exponential(arrival[1],(num_packet,num_source))
            elif arrival[0] == "deterministic":
                self.arr = np.ones(num_packet,num_source)*arrival[1]

            self.arr = np.cumsum(self.arr,0)


            return
    class Scheduler(object):
        def __init__(self):
            pass


if __name__ == "__main__":
    net = Network()
    net.generateSampleTimes(num_packet=10000)
    net.num_source
