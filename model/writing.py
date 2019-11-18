from measures import entropy, edit_distance, string_complexity
import numpy as np

def outputting(gen,ts,agents,freq,memory,positions,out,directory,run,optimization,exploration):
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
	complex_out = [string_complexity(i) for i in ag_soll]
	prob_ent_out = [entropy(i) for i in pos_pr]
	prob_str_out = list(set([len(i) for i in pos_pr]))
	prob_len_out = [len(i) for i in pos_pr]
	
	solu_pool = len(list(set(ag_soll)))
	prob_pool = len(list(set(pos_pr)))
	pop_size = len(agents)
	lev = np.sum(np.asarray(edit_out))/len(edit_out)
	lev_norm = np.sum(np.asarray(edit_norm_out))/len(edit_norm_out)
	s_len = np.sum(np.asarray(len_out))/len(len_out)
	p_len = np.sum(np.asarray(prob_str_out))/len(prob_str_out)
	ent = np.sum(np.asarray(ent_out))/len(ent_out)
	p_ent = np.sum(np.asarray(prob_ent_out))/len(prob_ent_out)
	sol_complexity = np.sum(np.asarray(complex_out))/len(complex_out)

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
		print('String Complexity: ', sol_complexity)
		print('Problem Length: ', np.sum(np.asarray(prob_str_out))/len(prob_str_out))