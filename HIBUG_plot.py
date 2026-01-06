import matplotlib.pyplot as plt

def param_string(pwt):
	return f"(w: {pwt.width}, |Q|: {pwt.q}, n: {pwt.n})"

def tree_size_distribution(pwt,nbins = 10):
	x = [len(pwt.treelist[i]) for i in pwt.treelist]
	plt.figure()  
	plt.hist(x,bins=nbins,log=True)
	plt.title("Tree Size Distribution "+param_string(pwt))
	plt.xlabel("tree size")
	plt.ylabel("log(frequency)")
	plt.pause(0.1)
	plt.show(block=False) 
	
def tree_distance_distribution(pwt,nbins = 10):
	x = [pwt.path_length[i] for i in pwt.path_length]
	m = max(x)
	if(m<nbins):
		nbins = m
	plt.figure()
	plt.hist(x,bins=nbins)
	plt.title("Tree Size Distribution "+param_string(pwt))
	plt.xlabel("path length")
	plt.ylabel("frequency")
	plt.pause(0.1)
	plt.show(block=False) 
	
def treeloop_distance_distribution(pwt,nbins = 10):
	x = [pwt.path_length[i]+len(pwt.looplist[pwt.loops[pwt.mapping[pwt.trees[i]]]]) for i in pwt.path_length]
	m = max(x)
	if(m<nbins):
		nbins = m
	plt.figure()  
	plt.hist(x,bins=nbins,log=True)
	plt.title("Tree and Adjacent Loop Size Distribution "+param_string(pwt))
	plt.xlabel("path length")
	plt.ylabel("log(frequency)")
	plt.pause(0.1)
	plt.show(block=False) 
	
def tree_node_distribution(pwt,nbins = 10):
	x = [len(pwt.previous[i]) if i in pwt.previous else 0 for i in pwt.trees]
	m = max(x)
	if(m<nbins):
		nbins = m
	plt.figure()  
	plt.hist(x,bins=nbins,log=True)
	plt.title("Distribution of Tree Node Sizes "+param_string(pwt))
	plt.xlabel("node size")
	plt.ylabel("log(frequency)")
	plt.pause(0.1)
	plt.show(block=False) 
	
def hamming_distance_distributino(pwt,nbins = 10):
	x = pwt.hamming.values()
	m = max(x)
	if(m<nbins):
		nbins = m
	plt.figure()  
	plt.hist(x,bins=nbins)
	plt.title("Distribution Hamming Distances "+param_string(pwt))
	plt.xlabel("hamming distance")
	plt.ylabel("frequency")
	plt.pause(0.1)
	plt.show(block=False) 
	
def generic_histogram(x,title="",nbins=10,log=False):
	plt.figure()  
	plt.hist(x,bins=nbins)
	plt.title(title)
	plt.pause(0.1)
	plt.show(block=False) 
	
def generic_line_plot(x,title="",log=""):
	plt.figure()  
	if(log==""):
		plt.plot(x.keys(),x.values())
	elif(log=="semilogx"):
		plt.semilogx(x.keys(),x.values())
	elif(log=="semilogy"):
		plt.semilogy(x.keys(),x.values())
	elif(log=="loglog"):
		plt.loglog(x.keys(),x.values())
	plt.title(title)
	plt.pause(0.1)
	plt.show(block=False) 
	
def generic_scatter_plot(x,y,s=1,title=""):
	plt.figure()  
	plt.scatter(x,y,s=s)
	plt.title(title)
	plt.pause(0.1)
	plt.show(block=False) 