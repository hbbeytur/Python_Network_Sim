import numpy as np
import math

class Network(object):
    def __init__(self,num_source = 5,num_server = 1,num_packet = 1000,arrival = ("poisson",[1]*5),service = ("exponential",[0.1]*5),queue = "FCFS",preemption = False,scheduler = "MAF"):

        self.packet_generator(num_packet,num_source,arrival)
        self.Queue = self.Queue(queue,num_source)
        self.Service = self.Service(num_source,num_packet,num_server,service)


    class Queue(object): # Stores arrival time of waiting packets
        def __init__(self,queue,num_source):
            self.Qtype = queue
            self.waiting = [[]]*num_source
        def putin(self,source_id,packet):
            if self.Qtype == "FCFS":
                self.waiting[source_id] = packet + self.waiting[source_id]
            elif self.Qtype == "LCFS":
                self.waiting[source_id] = self.waiting[source_id] + packet
        def takeout(self,source_id):
            if self.waiting[source_id]:
                return self.waiting[source_id].pop()
            else: return -1

    def packet_generator(self,num_packet,num_source,arrival,seed = 0):
        if arrival[0] == "poisson":
            self.arr = np.random.exponential(arrival[1],(num_packet,num_source))
        elif arrival[0] == "deterministic":
            self.arr = np.ones((num_packet,num_source))*arrival[1]

        self.arr = np.cumsum(self.arr,0)
        self.generatecontrolinstances(num_source, num_packet,self.arr)

        self.arr = np.insert(self.arr,0,0,axis=0)
        self.arr = self.arr.T
    def generatecontrolinstances(self,num_source,num_packet,arr):
        b = arr.ravel()
        index = np.mod(b.argsort(),num_source)
        time = b.sort()
        controlSteps =[time.tolist(),index.tolist()]

    class Scheduler(object):
        def __init__(self):
            pass

    class Service(object):
        def __init__(self,num_source,num_packet,num_server,service,seed = 15):
            self.arg = [num_source,num_packet,num_server,service,seed]
            if service[0] == "exponential":
                self.servicetime = np.random.exponential(service[1],(num_packet,num_source))
            elif service[0] == "determisinistic":
                self.servicetime = np.ones((num_packet, num_source)) * service[1]
            self.servicetime = self.servicetime.T.tolist()

        def time(self,source_id):
            if not self.servicetime[source_id]:
                self.__init__(*self.arg)
            else: return self.servicetime[source_id].pop()

    def controller(self):





if __name__ == "__main__":
    net = Network(arrival=("deterministic",[1]*5))

