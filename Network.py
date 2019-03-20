import numpy as np
import math

class Network(object):
    def __init__(self,num_source = 5,num_server = 1,num_packet = 1000,arrival = ("poisson",[1]*5),service = ("exponential",[0.1]*5),queue = "FCFS",preemption = False,scheduler = "MAF"):

        self.num_source = num_source
        self.num_packet = num_packet
        self.arrival = arrival
        self.service = service
        self.queue = queue
        self.preemption = preemption
        self.scheduler = scheduler

        self.packet_generator(num_packet,num_source,arrival)
        self.Queue = self.Queue(queue,num_source)
        self.Service = self.Service(num_source,num_packet,num_server,service)
        self.Scheduler = self.Scheduler(scheduler,preemption,num_source,self)

        self.arrival = []
        self.story = [[[0,0]]]*num_source
        self.departure = math.inf
        self.termination = False

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
        def nextvalue(self,source_id):
            return self.waiting[source_id][-1]
        def preempt(self,source_id,packet):
            self.waiting[source_id] = self.waiting[source_id] + packet


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
        self.controlSteps = np.concatenate([[time],[index]]).T.tolist()
    def store(self,source_id,arrival,departure):
        self.story[source_id] = self.story[source_id] + [[arrival,departure]]

    class Scheduler(object):
        def __init__(self,scheduler,preemption,num_source,network):
            self.scheduler = scheduler
            self.num_source = num_source
        def nextmove(self,time):
            if self.scheduler == "MAF":
                return self.MAF(time)
            elif self.scheduler == "MAD":
                return self.MAD(time)
        def MAF(self,time):
            self.ins_age = [0]* self.num_source
            for i in range(self.num_source -1):
                if network.Queue.nextvalue(i) > network.story[i][-1][0]: # If waiting packet is age-effective
                    self.ins_age[i] = time - network.story[i][-1][0] # This should be always positive
            return np.argmax(self.ins_age)
        def MAD(self,time):
            pass

    class Service(object):
        def __init__(self,num_source,num_packet,num_server,service,seed = 15):
            self.arg = [num_source,num_packet,num_server,service,seed]

            self.id = -1

            if service[0] == "exponential":
                self.servicetime = np.random.exponential(service[1],(num_packet,num_source))
            elif service[0] == "determisinistic":
                self.servicetime = np.ones((num_packet, num_source)) * service[1]
            self.servicetime = self.servicetime.T.tolist()

        def time(self,source_id):
            if not self.servicetime[source_id]:
                self.__init__(*self.arg)
            else: return self.servicetime[source_id].pop()



    def newService(self,currenttime,source_id):
        self.arrival = self.Queue.takeout(source_id)
        self.departure = currenttime + self.Service.time(source_id)
        self.Service.id = source_id

    def completeService(self):
        self.store(source_id, self.arrival, currenttime)  # Complete service
        self.Service.id = -1
        self.departure = math.inf

    def controller(self):
        if not self.controlSteps:
            print("END OF THE SIMULATION")
            self.termination = True
            return 0

        if self.controlSteps[-1][0] < self.departure: # Controls whether arrival instance or departure
            (currenttime, source_id) = self.controlSteps.pop(0)
            self.Queue.putin(source_id,currenttime) # Put new arrival into queue
        else: # departure
            (currenttime, source_id) = (self.departure,self.Service.id)
            self.completeService()

        self.next_id = self.Scheduler.nextmove(currenttime)
        if (self.Service.id < 0):
            self.newService(currenttime, next_id)
        elif self.preemption:
            old_arrival = self.arrival
            old_id = self.Service.id
            self.newService(currenttime,next_id)
            self.Queue.preempt(old_id,old_arrival)
        else:
            pass
    def run(self):
        while self.termination:
            self.controller()


if __name__ == "__main__":
    net = Network()
    net.run()

