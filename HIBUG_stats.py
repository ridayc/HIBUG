import pwtloop

class MStats():
	def __init__(self,window_size,state_space,tape_size,rep,output=1,offset=""):
		self.tree_sizes = dict()
		self.loop_sizes = dict()
		self.hamming = dict()
		self.weights = dict()
		self.path_lengths = dict()
		self.node_sizes = dict()
		self.tlratio = [0,0]
		self.rep = rep
		self.w = window_size
		self.q = state_space
		self.n = tape_size
		self.offset = offset
		self.run(self.rep,output)
		
	def iteration(self):
		pwt = pwtloop.PWT(pwtloop.random_truth_table_set(self.w,self.q),pwtloop.random_state_table_set(self.w,self.q),self.offset)
		pwt.connectivity(self.n)
		pwt.root_distance()
		pwt.hamming_map()
		t = pwt.treetot()
		s = 2**self.n*self.q-t
		self.tlratio[0]+=t
		self.tlratio[1]+=s
		accumulate_length(pwt.treelist,self.tree_sizes)
		accumulate_length(pwt.looplist,self.loop_sizes)
		accumulate_value(pwt.hamming,self.hamming)
		accumulate_value(pwt.weight,self.weights)
		accumulate_value(pwt.path_length,self.path_lengths)
		accumulate_value(pwt.tree_node_sizes(),self.node_sizes)
		
	def run(self,rep,output):
		for i in range(rep):
			if(i%output==output-1):
				print("Iteration "+str(i))
			self.iteration()
				

def accumulate_length(lname1,lname2,norm=1):
	for i in lname1:
			if(len(lname1[i]) not in lname2):
				lname2[len(lname1[i])] = norm
			else:
				lname2[len(lname1[i])]+=norm
				
def accumulate_value(lname1,lname2,norm=1):
	for i in lname1:
			if(lname1[i] not in lname2):
				lname2[lname1[i]] = norm
			else:
				lname2[lname1[i]]+=norm
				
def normalize(l,n):
	return {i:l[i]/n for i in l}