# -*- coding: utf-8 -*-
"""
ABM for "Escaping Optimization Traps".

@author: James Winters
"""
from measures import *
from graphs import *
from problemspace import *
from ag_init import *
from writing import *

def simulation(n,generations,trans_param,optimization,exploration,directory,run,out,pspace):
	"""
	Calls the function to procedurally generate new problems that an agent can move to (within a single edit distance).

	Parameters
	----------
	n : int
		number of agents in population
	generations : int
		number of generations
	trans_param : float
		the probability of an agent receiving a transmitted solution at each time step
	optimization: float
		the strength of optimization parameter
	exploration: float
		the exploration threshold parameter
	directory: str
		the directory and file that the ouput will be written
	run: int
		the current run of a simulation
	out: boolean
		if TRUE, writes to directory; elif FALSE, prints output
	pspace: list
		list of probabilities for determining movement within a space of the same, longer, or shorter length problems.

	"""
	#Initialisation
	invent_param,del_param,mod_param,prob,agents,p_initial,positions,maps,mapp,TS,ag_map,ag_edges,memory = init(n=n)
	
	#Main for loop
	for gen in range(0,generations):
		for ts in TS:
			random.shuffle(agents)
			freq = {'delete':[],'modification':[],'invent':[],'transmit':[]}
			if ts == 0:
				for agent in agents:
					inherit = inheritance(agent,ag_map,ag_edges)
					seq = sequence_generator(dict(inherit[0]),inherit[1])
					ag_map.update({agent:inherit[0]})
					ag_edges.update({agent:inherit[1]})
					memory.update({agent:seq})
			for agent in agents:
				problem = positions[agent]
				ag_sol = memory[agent]
				ag_node = [i for i in ag_map[agent]]
				ag_links = [i for i in ag_edges[agent]]
				ag_original = ag_map[agent]
				mod_p = np.random.choice(['modification','none'],1,p=[mod_param,1-mod_param])
				inv_p = np.random.choice(['invent','none'],1,p=[invent_param,1-invent_param])
				tra_p = np.random.choice(['transmit','none'],1,p=[trans_param,1-trans_param])
				del_p = np.random.choice(['delete','none'],1,p=[del_param,1-del_param])
				fitness = {}
				solutions = {}
				nodies = {}
				linkies = {}

				if mod_p == ['modification']:
					ag_mod = modification(ag_links,ag_links)
					seq = sequence_generator(dict(ag_node),ag_mod)
					solving = edit_distance(str(seq),str(problem))
					fitness.update({'modification':solving})
					solutions.update({'modification':seq})
					nodies.update({'modification':ag_node})
					linkies.update({'modification':ag_mod})

				if inv_p == ['invent']:
					origi = [i for i in dict(ag_node)]
					ag_invent = invention(mapp,ag_node,ag_links)
					revis = [i for i in dict(ag_invent)]
					new_element = list(set(revis) - set(origi))
					connect_to = random.choice(origi)
					updated = [new_element[0],connect_to]
					random.shuffle(updated)
					ag_updates = [(updated[0],updated[1])]
					ag_links_update = ag_links + ag_updates
					seq = sequence_generator(dict(ag_invent),ag_links_update)
					solving = edit_distance(str(seq),str(problem))
					fitness.update({'invent':solving})
					solutions.update({'invent':seq})
					nodies.update({'invent':ag_invent})
					linkies.update({'invent':ag_links_update})
					mapp_list = [i[0] for i in mapp]
					mapp_update = list(set(new_element+mapp_list))

				if tra_p == ['transmit']:
					ag_learn = transmission(agents,agent,ag_map,ag_edges)
					seq = sequence_generator(dict(ag_learn[0]),ag_learn[1])
					solving = edit_distance(str(seq),str(problem))
					fitness.update({'transmit':solving})
					solutions.update({'transmit':seq})
					nodies.update({'transmit':ag_learn[0]})
					linkies.update({'transmit':ag_learn[1]})

				if del_p == ['delete']:
					ag_delete = deletion(ag_node,ag_links)
					seq = sequence_generator(dict(ag_node),ag_delete)
					solving = edit_distance(str(seq),str(problem))
					fitness.update({'delete':solving})
					solutions.update({'delete':seq})
					nodies.update({'delete':ag_node})
					linkies.update({'delete':ag_delete})

				stored_ld = edit_distance(str(ag_sol),str(problem))
				fitness.update({'stored':stored_ld})
				solutions.update({'stored':ag_sol})

				fitness_list = sorted(fitness, key=fitness.__getitem__)
				new_solution = solutions[fitness_list[0]]
				source = fitness_list[0]

				select = np.random.choice(['biased','stochastic'],1,p=[optimization,1-optimization])
				if select == ['biased']:
					new_ld = edit_distance(str(new_solution),str(problem))
					if new_ld < stored_ld:
						counts = freq[source]
						counts.append(source)
						freq.update({source:counts})
						node_mapping = nodies[source]
						edge_links = linkies[source]
						ag_map.update({agent:node_mapping})
						ag_edges.update({agent:edge_links})
						memory.update({agent:new_solution})
						if invent_param > 0.0:
							if len(mapp_update) > len(mapp_list):
								inv_dict = dict(ag_invent)
								mapp = mapp + [(new_element[0],inv_dict[new_element[0]])]
								if source != 'invent':
									del mapp[-1]
					else:
						ag_map.update({agent:ag_node})
						ag_edges.update({agent:ag_links})
						memory.update({agent:ag_sol})
						if invent_param > 0.0:
							if len(mapp_update) > len(mapp_list):
								inv_dict = dict(ag_invent)
								mapp = mapp + [(new_element[0],inv_dict[new_element[0]])]
								del mapp[-1]
				if select == ['stochastic']:
					nodies.update({'stored':ag_node})
					linkies.update({'stored':ag_links})
					random_choice = random.choice(fitness_list)
					new_solution = solutions[random_choice]
					node_mapping = nodies[random_choice]
					edge_links = linkies[random_choice]
					memory.update({agent:new_solution})
					ag_map.update({agent:node_mapping})
					ag_edges.update({agent:edge_links})
					if invent_param > 0.0:
						if len(mapp_update) > len(mapp_list):
							inv_dict = dict(ag_invent)
							mapp = mapp + [(new_element[0],inv_dict[new_element[0]])]
							if random_choice != 'invent':
								del mapp[-1]
				loc = positions[agent]
				new_loc = movement(prob=prob,loc=loc,pspace=pspace)
				norm_edit = decision(agent,memory,problem)
				if norm_edit > exploration:
					positions.update({agent:new_loc})
					if new_loc not in prob:
						prob.update({new_loc:['*','+','-']})
			
			outputting(gen,ts,agents,freq,memory,positions,out,directory,run,optimization,exploration)

#simulation(n=100,generations=100,trans_param=1.0,optimization=0.6,exploration=0.2,directory='singlerun.csv',run=0,out=False,pspace=[0.5,0.3,0.2])