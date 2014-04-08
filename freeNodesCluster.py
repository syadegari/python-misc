# Script for querying the free nodes on the cluster (works for PBS)
# Command line: python freeNodesCluster.py
# Number of free nodes =  7
# n12-03 48 12
# n12-06 48 2
# n12-07 48 4
# n12-61 8 4
# n12-69 8 4
# n12-73 32 32
# n12-74 32 16
################################################################################
# M.A.I.N.
import shlex
import subprocess as sp
import numpy as np
file_temp = 'file.temp'
No_free_proc = {}
p = sp.Popen(['pbsnodes -l free'], shell = True, stdout = sp.PIPE)
N_freeNodes = 0
list_freeNodes =[]
for line in p.stdout:
	 list_freeNodes.append(line.split()[0])
 	 if int(list_freeNodes[-1][-2]+list_freeNodes[-1][-1])> 0:
		 if int(list_freeNodes[-1][-2:])> 0:		 
			 N_freeNodes = N_freeNodes + 1
	 else:
		 if list_freeNodes != []:
			 list_freeNodes.pop()


# N_nodes = raw_input("How many nodes do you like to allocate? ")
# print list_freeNodes
# allocatedNodes = ''
# list_freeNodes = np.random.permutation(list_freeNodes)
list_freeNodes = list(list_freeNodes)
N_freeNodes = 0
for node in list_freeNodes:
	p = sp.Popen(['pbsnodes '+node], shell = True, stdout = sp.PIPE)
	n_j = 0 
	for line in p.stdout:
		 line_temp = line.split()
		 if len(line_temp)!= 0 and line_temp[0]== 'np':
		 	 n_p = int(line_temp[-1])
		 if len(line_temp)!= 0 and line_temp[0]== 'jobs':
		 	 n_j = len(line_temp) - 2
	n_f = n_p - n_j #  number of free processors on the node
	if n_f > 0:
		N_freeNodes += 1
		No_free_proc.update({node:[n_p, n_f]}) 

dictSort = No_free_proc.keys()
dictSort.sort()

print 'Number of free nodes = ', N_freeNodes
for i in dictSort:
	print  i,  No_free_proc[i][0] , No_free_proc[i][1]

