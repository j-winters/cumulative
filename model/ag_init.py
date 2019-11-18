import random
from itertools import permutations, chain, combinations
from problemspace import generate_binary,local_space
from graphs import sequence_generator, node_generator

def agent_generator(agents,mapp,ag_map,ag_edges,memory):
	for ag in agents:
		node_number = [3,4,5]
		initial_sols = random.sample(mapp,k=random.choice(node_number))
		node_list = [node[0] for node in initial_sols]
		node_permute = list(permutations(node_list, r=2))
		node_edges = random.sample(node_permute,k=len(initial_sols)-1)
		ag_map.update({ag:initial_sols})
		ag_edges.update({ag:node_edges})
		sequence = sequence_generator(dict(initial_sols),node_edges)
		memory.update({ag:sequence})
	return ag_map, ag_edges, memory

def init(n):
	invent_param = 1.0
	del_param = 1.0
	mod_param = 1.0
	prob = {'00':['*','+'],'01':['*','+'],'10':['*','+'],'11':['*','+']}
	agents = [i for i in range(n)]
	p_initial = generate_binary(2)
	positions = local_space(p_initial,agents)
	maps = node_generator({})
	mapp = list(maps.items())
	TS = [ts for ts in range(0,10)]
	ag_map,ag_edges,memory = agent_generator(agents,mapp,dict(),dict(),dict())
	return invent_param,del_param,mod_param,prob,agents,p_initial,positions,maps,mapp,TS,ag_map,ag_edges,memory