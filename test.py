import HIBUG
import HIBUG_plot
import HIBUG_stats
import random

window_size = 3
state_space = 5 #2**statespace parity states
n = 17
rep = 1
output=100
'''
test = pwt_stats.MStats(window_size,state_space,n,rep,output)
d = 1/2**n/rep/state_space
print("Tree to Loop Point Ratio\n Tree Points: "+str(test.tlratio[0]*d)+"\n Loop Points: "+str(test.tlratio[1]*d)+"\n Group Ratio T/L: "+str(test.tlratio[0]/test.tlratio[1]))
pwt_plot.generic_line_plot(dict(sorted(test.tree_sizes.items())),"Tree Sizes","loglog")
pwt_plot.generic_line_plot(dict(sorted(test.loop_sizes.items())),"Loop Sizes","loglog")
pwt_plot.generic_line_plot(dict(sorted(test.hamming.items())),"Hamming Distances")
pwt_plot.generic_line_plot(dict(sorted(test.weights.items())),"Hamming Weights")
pwt_plot.generic_line_plot(dict(sorted(test.path_lengths.items())),"Path Lengths","semilogy")
pwt_plot.generic_line_plot(dict(sorted(test.node_sizes.items())),"Tree Node Sizes","semilogy")
#'''
#'''
test = HIBUG.HIBUG(m=state_space,ccg=window_size)
test.connectivity(n)
test.root_distance()
test.hamming_map()
'''
for i in test.looplist.values():
	a = "["
	for j in i:
		tape = str(HIBUG.digits_base(j%2**n,2,n))+"/"+str(HIBUG.digits_base(int(j/2**n),2,state_space))
		a+=tape+","
	a+="]"
	print(a)
'''
#x = [test.weight[i] for i in test.trees]
#y = [test.path_length[i]+0.5-random.random())*0.5 for i in test.trees]
print(len(test.loops))
x = [test.weight[i] +(0.5-random.random())*0.5 for i in test.loops]
y = [len(test.looplist[test.loops[i]]) for i in test.loops]
HIBUG_plot.generic_scatter_plot(x,y,0.2)
HIBUG_plot.generic_histogram([test.weight[i] for i in test.loops],"",range(n))
HIBUG_plot.generic_histogram(test.weight,"",range(n))
#'''
HIBUG_plot.plt.show()