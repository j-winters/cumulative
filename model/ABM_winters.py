import math
import numpy as np
import networkx as nx
import os
import random
import editdistance
from itertools import permutations, chain, combinations
import string
import ast

def entropy(string):
	prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
	entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
	return entropy

def edit_distance(s1, s2):
	LD = editdistance.eval(s1, s2)
	return LD

def string_complexity(string):
	complexity = entropy(string) * len(string)
	return complexity

def sequence_generator(maps,edges):
	sequence = nx.DiGraph()
	for node in maps:
		sequence.add_node(node,state=maps[node])
	dic_state =  nx.get_node_attributes(sequence,'state')
	for ed1,ed2 in edges:
		weighting = (dic_state[ed1] + dic_state[ed2]) / 2
		if weighting == 0.5:
			rounded = random.choice([0,1])
		else:
			rounded = int(round(weighting))
		sequence.add_edge(ed1,ed2, weight = rounded)
	weights = nx.get_edge_attributes(sequence,'weight')
	weight_sequence = sorted(weights)
	seq = [weights[i] for i in weight_sequence]
	out = ''.join(str(i) for i in seq)
	return out

def node_generator(mapping):
	state = np.linspace(0,1,11)
	if mapping == {}:
		nodes = [str(i) for i in range(0,5)]
		maps = {key:random.choice(state) for key in nodes}
	if mapping != {}:
		for i in mapping:
			if mapping[i] == []:
				mapping.update({i:random.choice(state)})
				maps = mapping
	return maps

def deletion(nodes,links):
	linkage = links
	if len(linkage) > 2:
		link_choice = random.choice(linkage)
		linkage.remove(link_choice)
	return linkage	

def invention(all_nodes,ag_nodes,ag_links):
	node_mappings = dict(all_nodes)
	nodes = [i for i in node_mappings]
	nodes.append(str(len(nodes)))
	selection = random.choice(nodes)
	agent_nodes = [i[0] for i in ag_nodes]
	while selection in agent_nodes:
		selection = random.choice(nodes)
	if selection in [i for i in node_mappings]:
		value = node_mappings[selection]
		map_entry = [i for i in ag_nodes]
		map_entry.append((selection,value))
	else:
		state = np.linspace(0,1,11)
		value = random.choice(state)
		map_entry = [i for i in ag_nodes]
		map_entry.append((selection,value))
	return map_entry

def modification(nodes,links):
	node_list = list(set(list(chain(*nodes))))
	possibilities = list(permutations(node_list,2))
	choices = list(set(possibilities) - set(links))
	if len(choices) == 0:
		node_links = links
	else:
		node_choice = random.sample(choices,k=1)
		node_links = links + node_choice
	return node_links

def transmission(agents,agent,mapps,edgee):
	list_of_agents = [i for i in agents if i!=agent]
	sender = np.random.choice(list_of_agents,1)
	sender = sender[0]
	sender_node_value = list(mapps[sender])
	sender_edge_value = list(edgee[sender])
	observation = nx.DiGraph()
	for node in sender_node_value:
		observation.add_node(node[0],state=node[1])
	dic_state = nx.get_node_attributes(observation,'state')
	for ed1,ed2 in sender_edge_value:
		weighting = (dic_state[ed1] + dic_state[ed2]) / 2
		rounded = int(round(weighting))
		observation.add_edge(ed1,ed2, weight = rounded)

	inference = nx.DiGraph()
	source_value = sender_edge_value[0][0]
	compressor = nx.shortest_path(observation,source=source_value,weight=None,method='dijkstra')
	for com in compressor:
		inference.add_node(com,state=dic_state[com])
		paths = compressor[com]
		if len(paths) > 1:
			nx.add_path(inference,paths)
	dic_states = nx.get_node_attributes(inference,'state')
	ls_states = [(i,dic_states[i]) for i in dic_states]
	ed = nx.edges(inference)
	return ls_states, list(ed)

def inheritance(agent,mapps,edgee):
	sender = agent
	sender_node_value = list(mapps[sender])
	sender_edge_value = list(edgee[sender])
	observation = nx.DiGraph()
	for node in sender_node_value:
		observation.add_node(node[0],state=node[1])
	dic_state =  nx.get_node_attributes(observation,'state')
	ls_state = dic_state
	ls_edge = sender_edge_value
	for ed1,ed2 in ls_edge:
		weighting = (dic_state[ed1] + dic_state[ed2]) / 2
		rounded = int(round(weighting))
		observation.add_edge(ed1,ed2, weight = rounded)

	inference = nx.DiGraph()
	source_value = sender_edge_value[0][0]
	compressor = nx.shortest_path(observation,source=source_value,weight=None,method='dijkstra')
	for com in compressor:
		inference.add_node(com,state=dic_state[com])
		paths = compressor[com]
		if len(paths) > 1:
			nx.add_path(inference,paths)
	dic_states = nx.get_node_attributes(inference,'state')
	ls_states = [(i,dic_states[i]) for i in dic_states]
	ed = nx.edges(inference)
	ls_edges = list(ed)
	return ls_states,ls_edges

def generate_binary(n):
	bin_arr = range(0, int(math.pow(2,n)))
	bin_arr = [bin(i)[2:] for i in bin_arr]
	max_len = len(max(bin_arr, key=len))
	bin_arr = [i.zfill(max_len) for i in bin_arr]

	return bin_arr

def space(n):
	space = [i for i in range(n)]
	return space

def local_space(initial,agents):
	pos = [random.choice(initial) for i in range(len(agents))]
	positions = dict(zip(agents, pos))
	return positions

def prob_space_reader(fname):
	with open(fname+'.txt','r') as inputs:
		prob = inputs.read()
		prob = eval(prob)
	return prob

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

def simulation(n,generations,trans_param,optimization,exploration,directory,run,out,pspace):
	invent_param = 1.0
	del_param = 1.0
	mod_param = 1.0
	prob = {'00':['*','+'],'01':['*','+'],'10':['*','+'],'11':['*','+']}
	agents = [i for i in range(n)]
	p_initial = generate_binary(2)
	positions = local_space(p_initial,agents)
	maps = node_generator({})
	mapp = list(maps.items())
	ag_map = dict()
	ag_edges = dict()
	memory = dict()
	TS = [ts for ts in range(0,10)]
	ag_map,ag_edges,memory = agent_generator(agents,mapp,dict(),dict(),dict())

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
				if len(loc) == 2:
					move_poss = np.random.choice(prob[loc],1,p=[0.75,0.25])
				else:
					move_poss = np.random.choice(prob[loc],1,p=pspace)
				if move_poss == ['*']:
					st_locs = [i for i in range(len(loc))]
					val_loc = random.choice(st_locs)
					value = loc[val_loc]
					if value == '0':
						new_loc = loc[:val_loc] + '1' + loc[val_loc+1:]
					elif value == '1':
						new_loc = loc[:val_loc] + '0' + loc[val_loc+1:]
				if move_poss == ['+']:
					st_locs = [i for i in range(len(loc)+1)]
					val_loc = random.choice(st_locs)
					try:
						value = loc[val_loc]
						if value == '0':
							new_loc = loc[:val_loc] + '1' + loc[val_loc:]
						elif value == '1':
							new_loc = loc[:val_loc] + '0' + loc[val_loc:]
					except IndexError:
						new_loc = loc + random.choice(['0','1'])
				if move_poss == ['-']:
					st_locs = [i for i in range(len(loc))]
					val_loc = random.choice(st_locs)
					value = loc[val_loc]
					new_loc = loc[:val_loc] + loc[val_loc+1:]

				sol_len = len(str(memory[agent]))
				prob_len = len(str(problem))
				maxi = max([sol_len,prob_len])
				norm_edit = edit_distance(str(memory[agent]),str(problem))/maxi
				if norm_edit > exploration:
					positions.update({agent:new_loc})
					if new_loc not in prob:
						prob.update({new_loc:['*','+','-']})
			del_freq = len(freq['delete'])
			tra_freq = len(freq['transmit'])
			inv_freq = len(freq['invent'])
			mod_freq = len(freq['modification'])
			ag_soll = [memory[agent] for agent in agents]
			pos_pr = [positions[agent] for agent in agents]
			edit_out = [edit_distance(i,j) for i,j in zip(ag_soll,pos_pr)]
			edit_norm_out = [edit_distance(i,j)/len(max([i,j], key=len)) for i,j in zip(ag_soll,pos_pr)]
			len_out = [len(i) for i in ag_soll]
			ent_out = [entropy(i) for i in ag_soll]
			prob_ent_out = [entropy(i) for i in pos_pr]
			prob_str_out = list(set([len(i) for i in pos_pr]))
			prob_len_out = [len(i) for i in pos_pr]
			edit_LD = np.sum(np.asarray(edit_norm_out))/len(edit_norm_out)
			
			solu_pool = len(list(set(ag_soll)))
			prob_pool = len(list(set(pos_pr)))
			pop_size = len(agents)
			lev = np.sum(np.asarray(edit_out))/len(edit_out)
			lev_norm = np.sum(np.asarray(edit_norm_out))/len(edit_norm_out)
			s_len = np.sum(np.asarray(len_out))/len(len_out)
			p_len = np.sum(np.asarray(prob_str_out))/len(prob_str_out)
			ent = np.sum(np.asarray(ent_out))/len(ent_out)
			p_ent = np.sum(np.asarray(prob_ent_out))/len(prob_ent_out)
			sol_complexity = ent * s_len

			if out == True:
				with open(directory,'a') as output:
					output.write(str(run)+';'+str(gen)+';'+str(ts)+';'+str(pop_size)+';'+str(optimization)+';'+str(exploration)+';'+str(solu_pool)+';'+str(prob_pool)+';'+str(s_len)+';'+str(p_len)+';'+str(ent)+';'+str(p_ent)+';'+str(lev)+';'+str(lev_norm)+';'+str(tra_freq)+';'+str(inv_freq)+';'+str(del_freq)+';'+str(mod_freq)+';'+str(sol_complexity)+'\n')
			
			else:
				print('Gen:',gen)
				print('TS: ',ts)
				print('modification:',len(freq['modification']))
				print('Transmit:',len(freq['transmit']))
				print('Invent:',len(freq['invent']))
				print('Delete:',len(freq['delete']))
				print('Solution Pool Size: ',len(list(set(ag_soll))))
				print('LD(Norm): ', np.sum(np.asarray(edit_norm_out))/len(edit_norm_out))
				print('String length: ', np.sum(np.asarray(len_out))/len(len_out))
				print('String Entropy (Average): ', np.sum(np.asarray(ent_out))/len(ent_out))
				print('String Complexity: ', ent * s_len)
				print('Problem Length: ', np.sum(np.asarray(prob_str_out))/len(prob_str_out))
