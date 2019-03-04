import numpy as np

class Network(object):
    def __init__(self):

        self.num_server = 1
        self.num_source = 5

    def generateSampleTimes(self,num_packet = 1000, type = "poisson", rate="default"):
        if rate == "default":
            rate = [1]*self.num_source

        self.num_packet = num_packet

        if type == "poisson":
            self.arr_TS = np.random.exponential(rate,(num_packet,self.num_source))
        elif type == "deterministic":
            self.arr_TS = np.ones(num_packet,self.num_source)*1

        self.arr_TS = np.cumsum(self.arr_TS,0)



if __name__ == "__main__":
    net = Network()
    net.generateSampleTimes(num_packet=10000)
    net.num_source
