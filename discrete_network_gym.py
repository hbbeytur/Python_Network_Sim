## Description:
# In this simulator, a server is giving service to a given number of clients. Depending on the sampling action taken by the learning agent, the

import numpy as np
import math

class netmodel(object):
	def __init__(self,num_client,s_episode,tx_prob,queueType = 'FCFS'):
		self.num_client = num_client
		self.s_episode = s_episode
		self.tx_prob = tx_prob
		self.queueType = queueType

		# Preparing recording variables

		self.queueLength = [0]*num_client # The number of packets waiting in the queue for every client
		self.states_ages = np.zeros((num_client,s_episode)) # Status age record along whole episode for each client
		self.queues = [[] for i in range(num_client)] # the gen. timestamps of the packets are stored in the queue of every client
		self.reception = [[0] for i in range(num_client)] # the reception time of the packets for each client
		self.tx = np.random.binomial(1,tx_prob,s_episode) # Pre-generated events of transmission along the trial

		self.t = 0 # carries the step info. (time)

	def step(self,action):
		if self.queueType == 'FCFS':
			self.step_FCFS(action)
		elif self.queueType == 'LCFS':
			self.step_LCFS(action)

	def step_FCFS(self,action):
		self.t += 1


		for id in range(self.num_client):
			if action[id]:
				self.queues[id].append(self.t)


		tx_event = self.tx[self.t-1]
		sent = -1
		tx_id = action[self.num_client]
		if tx_event and self.queues[tx_id]:
			self.reception[tx_id].append(self.queues)






	def step_LCFS(self,action):
		...