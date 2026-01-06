# HI-BUG (Heterogeneous Implicit Bounded Universal Graph)
# This model takes a polynomially time and space bounded mixing and control machine tuple (potential universal computation under the constraints) and infers a deterministic directed connectivity graph for transitions of a finite periodic state band and |Q|-state internal memory
import random
import math

class HIBUG():
	def __init__(self,m=1,ccg=3,sigma_ca=2,sigma_tm=2):
		self.m = m
		self.sigma_ca = sigma_ca
		self.sigma_tm = sigma_tm
		# initiation of a simple generator model if none is given
		if(not isinstance(ccg,CCG)):
			self.ccg = create_simple_CCG(2**ccg,m)
			self.sigma_tm = 2**m
			self.m = 1
			sigma_ca = 2
		else:
			self.ccg = ccg

	def map(self,n):
		self.n = n
		l_ca = self.sigma_ca**n
		l_tm = self.sigma_tm**self.m
		self.transitions = [None]*l_ca*l_tm
		ca_band = [0]*n
		tm_band = [0]*self.m
		for i in range(l_tm):
			for j in range(l_ca):
				ca_band[:] = digits_base(j,self.sigma_ca,n)
				tm_band[:] = digits_base(i,self.sigma_tm,self.m)
				self.ccg.iter(ca_band,tm_band)
				self.transitions[i*l_ca+j] = revert_digits(tm_band,self.sigma_tm)*l_ca+revert_digits(ca_band,self.sigma_ca)
	
	def connectivity(self,n):
		self.map(n)
		self.previous = dict()
		self.loops = dict()
		self.roots = dict()
		self.trees = dict()
		self.visited = dict()
		self.looplist = dict()
		self.treelist = dict()
		self.eden = dict()
		l_ca = self.sigma_ca**n
		l_tm = self.sigma_tm**self.m
		# go through each possible tape and machine state configuration
		for i in range(len(self.transitions)):
			current = i
			# only work on configurations that haven't been processed yet
			if(not(current in self.visited)):
				self.visited[current] = 1
				next = self.transitions[current]
				if(next in self.previous):
					self.previous[next].append(current)
				else:
					self.previous[next] = [current]
				# entry configuration loops to itself, aka it's a terminal loop/point
				if(next==current):
					self.loops[current] = current
					self.looplist[current] = [current]
				# we check if the new configuration points to an existing tree or loop
				elif(next in self.visited):
					# check if the next point belongs to a tree or a loop
					# if the next point belongs to a loop, the current point has to be the root of a tree with no other points at the moment
					if(next in self.loops):
						self.roots[current] = 1
						self.trees[current] = current
						self.treelist[current] = [current]
					# else the next point belongs to a tree, and the current point belongs to the same tree
					else:
						self.trees[current] = self.trees[next]
						self.treelist[self.trees[next]].append(current)
				# otherwise the next point has not been visited and we need to follow the point until we find a loop (finding a loop is guaranteed)
				else:
					while(True):
						# it is sad there is no word for this in English :(
						# we check one position further ahead to be able to identifiy root points
						overnext = self.transitions[next]
						self.visited[next] = 1
						if(overnext in self.previous):
							self.previous[overnext].append(next)
						else:
							self.previous[overnext] = [next]
						# check for terminal loops
						if(next==overnext):
							self.loops[next] = next
							self.looplist[next] = [next]
							# the previous point becomes the root of a tree once a loop is reached
							self.roots[current] = 1
							self.trees[current] = current
							self.treelist[current] = [current]
							# we at this point go backwards to label all points of the path as beloning to this root. There is guaranteed only one previous point for each point on the path per design of the walkthrough algorithm
							previous = current
							while(previous in self.previous):
								previous = self.previous[previous][0]
								self.trees[previous] = current
								self.treelist[current].append(previous)
							break
						elif(overnext in self.visited):
							# check if the next point belongs to a loop
							if(overnext in self.loops):
								self.roots[next] = 1
								self.trees[next] = next
								self.treelist[next] = [next]
								previous = next
								# backtrack new tree lable
								while(previous in self.previous):
									previous = self.previous[previous][0]
									self.trees[previous] = next
									self.treelist[next].append(previous)
							# check if the next point belongs to a tree
							elif(overnext in self.trees):
								treen = self.trees[overnext]
								self.trees[next] = treen
								self.treelist[treen].append(next)
								previous = next
								# backtrack tree lable
								while(previous in self.previous):
									previous = self.previous[previous][0]
									self.trees[previous] = treen
									self.treelist[treen].append(previous)
							# otherwise we encounter the trickiest case:
							# we have found a new loop
							else:
								# the point we are targeting is the entry point of the loop
								start = overnext
								self.visited[start] = 1
								self.loops[start] = start
								self.looplist[start] = [start]
								current = self.transitions[overnext]
								# loop forward from the start to mark all points as belonging to the loop
								while(current!=start):
									self.loops[current] = start
									self.looplist[start].append(current)
									current = self.transitions[current]
								# in case there was an entry point leading into the loop
								# if the start point has at least two previous points, this means it is a loop with a tree leading into it
								if(len(self.previous[start])>1):
									root = self.previous[start][0]
									self.roots[root] = 1
									self.trees[root] = root
									self.treelist[root] = [root]
									previous = root
									# backtrack new tree lable
									while(previous in self.previous):
										previous = self.previous[previous][0]
										self.trees[previous] = root
										self.treelist[root].append(previous)
							break
						# otherwise we need to move forward in the loop and store the previous marker
						else:
							current = next
							next = overnext
	
	def root_distance(self):
		totdist = 0
		self.path_length = dict()
		for i in self.roots.keys():
			marked = dict()
			start = i
			current = start
			# initial distance to root
			dist = 0
			self.path_length[start] = 0
			# implemented with single loop backtracking instead of recursion, because why not...
			while(start not in marked):
				if(current not in marked and current in self.previous):
					for j in range(len(self.previous[current])):
						if(self.previous[current][j] not in marked):
							current = self.previous[current][j]
							dist+=1
							self.path_length[current] = dist
							break
						if(j==len(self.previous[current])-1):
							marked[current] = 1
							current = self.transitions[current]
							dist-=1
						
				else:
					marked[current] = 1
					current = self.transitions[current]
					dist-=1

	def hamming_map(self):
		l = len(self.transitions)
		self.hamming = [0]*l
		self.weight = [0]*l
		l_ca = self.sigma_ca**self.n
		for i in range(l):
			ca_tape1  = digits_base(i%l_ca,self.sigma_ca,self.n)
			ca_tape2 = digits_base(self.transitions[i]%l_ca,self.sigma_ca,self.n)
			self.hamming[i] = sum([0 if ca_tape1[j]==ca_tape2[j] else 1 for j in range(self.n)])
			self.weight[i] = sum([1 if ca_tape2[j]==0 else 0 for j in range(self.n)])
	
	def tree_node_sizes(self):
		return {i:len(self.previous[i]) if i in self.previous else 0 for i in self.trees}
		
	def loop_node_sizes(self):
		return {i:len(self.previous[i])-1 if i in self.previous else 0 for i in self.loops}
		
	def treetot(self):
		return sum([len(self.treelist[i]) for i in self.treelist])

def digits_base(n,base,length):
	digits = [0]*length
	count = 1
	while(n>0):
		n,digits[-count] = divmod(n,base)
		count+=1
	return digits

def revert_digits(digits,base):
	v = 0
	for d in digits:
		v=v*base+d
	return v



# CCG (Coupled Configuration Generator)
# the machinistic generator class containing a coupled CA mixer and TM controller
class CCG():
	def __init__(self,mixer,controller):
		self.mixer = mixer
		self.controller = controller

	def iter(self,ca_band,tm_band,instance_param=None,ca_it=1):
		# this loop is an implicit reminder and control that the ca should be in parallel on all locations and simultaneous in execution
		# technically this is not a ca due to access to a common tm_band (but we can imagine each cell having access to its own copy of the tm_band. Would add complexity*len(tm_band))
		for i in range(ca_it):
			temp_ca = [0]*len(ca_band)
			for j in range(len(ca_band)):
				temp_ca[j] = self.mixer.iter(j,ca_band,tm_band)
			ca_band[:] = temp_ca
		self.controller.iter(ca_band,tm_band,instance_param)

# generic mixer class. Calculations here are pseudoparallel: Each cell is controlled by the "same" rule and all band updates happen simultaneously/are synchronized. Locality window depends on a location parameter. The location parameter itself could be used for computation, but that seems like it would only unneccessarily complicate analysis without real gain.
class CA_Mixer():
	def __init(self,wrapper_function):
		self.func = wrapper_function
	
	def iter(i,ca_band,tm_band):
		self.func(i,ca_band,tm_band,ca_param,tm_param)

class TM_Controller():
	def __init(self,wrapper_function):
		self.func = wrapper_function
	
	def iter(ca_band,tm_band,ca_param,tm_param):
		self.func(i,ca_band,tm_band,ca_param,tm_param)


class Simple_CA():
	def __init__(self,truth_table,offset=""):
		self.rule = truth_table
		self.width = int(math.log(len(self.rule[0]),2))
		if(offset==""):
			offset = -int(self.width/2)
		self.offset = offset

	def iter(self,i,ca_band,tm_band):
		n = len(ca_band)
		window = [ca_band[(i+self.offset+j)%n] for j in range(self.width)]
		return self.mix(window,tm_band[0])

	def mix(self,window,q):
		idx = revert_digits(window,2)
		return self.rule[q][idx]

class Simple_TM():
	def __init__(self,q):
		self.q = q

	def iter(self,ca_band,tm_band,instance_param):
		n = math.ceil(0.5+math.sqrt(0.25+2*self.q))
		temp = [0]*self.q
		for i in range(len(ca_band)):
			c = 0
			for j in range(n):
				for k in range(j):
					if(c<self.q):
						if((i+k)%j==0):
							temp[c]+=ca_band[i]
						c+=1
		for i in range(self.q):
			temp[i]%=2
		if(self.q>0):
			tm_band[0] =  revert_digits(temp,2)



def create_simple_CCG(width_2,q):
	if(q>0):
		ca = Simple_CA([random_truth_table(width_2) for i in range(2**q)])
	else:
		ca = Simple_CA([random_truth_table(width_2)])
	return CCG(ca,Simple_TM(q))


def generate_truth_table(values,init=""):
	if isinstance(values[0], list):
		truth = [init]*2**init[0]
		for i in values:
			truth[i[0]] = i[1]
	else:
		n = len(values)
		truth = [None]*n
		if((n & (n-1) == 0) and n != 0):
			for i in range(n):
				truth[i] = int(values[i])
		else:
			print("The length of the input needs to be a power of 2!")
	return truth

def random_bin_string(n):
	# generate
	bits = bin(random.getrandbits(n))[2:].zfill(n)
	return bits

def random_truth_table(n):
	bits = random_bin_string(n)
	return generate_truth_table(bits)
