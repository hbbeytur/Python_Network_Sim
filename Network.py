import numpy as np

class Network(object):
    def __init__(self,num_source = 5,num_server = 1,num_packet = 1000,arrival = ("poisson",[1]*5),service = ("exponential",[0.1]*5),queue = "FCFS",preemption = False,scheduler = "MAF"):

        self.generator = self.Packet_Generator(num_packet,num_source,arrival)
        # self.queue = self.Queue(queue)

    class Queue(object):
        def __init__(self):
            return
        def putin(self):
            return
        def takeout(self):
            return

    class Packet_Generator(object):
        def __init__(self,num_packet,num_source,arrival,seed = 0):
            if arrival[0] == "poisson":
                self.arr = np.random.exponential(arrival[1],(num_packet,num_source))
            elif arrival[0] == "deterministic":
                self.arr = np.ones((num_packet,num_source))*arrival[1]

            self.arr = np.cumsum(self.arr,0)
            self.arr = np.insert(self.arr,0,0,axis=0)

    class Scheduler(object):
        def __init__(self):
            pass


if __name__ == "__main__":
    net = Network(arrival=("deterministic",[1]*5))

