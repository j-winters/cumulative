import numpy as np
import random
from measures import edit_distance

def generate_binary(n):
	"""
	Calls the function to generate a space of binary sequences of N-length.

	Parameters
	----------
	n : int

	Returns
	-------
	[list]
		A list of binary strings of N-length.
	"""
	bin_arr = range(0, int(np.power(2,n)))
	bin_arr = [bin(i)[2:] for i in bin_arr]
	max_len = len(max(bin_arr, key=len))
	bin_arr = [i.zfill(max_len) for i in bin_arr]
	return bin_arr

def local_space(initial,agents):
	pos = [random.choice(initial) for i in range(len(agents))]
	return dict(zip(agents, pos))

def movement(prob,loc,pspace):
	"""
	Calls the function to procedurally generate new problems that an agent can move to (within a single edit distance).

	Parameters
	----------
	prob : dict
		key: loc [str]
		value: ['*','+','-']
	loc : str
		The current problem an agent is located at.
	pspace : list
		A list of floats which serve as the probabilities for choosing the value in prob[loc]

	Returns
	-------
	[str]
		A new location (i.e., a binary sequence) for an agent to possibly occupy.
	"""
	if len(loc) == 2:
		move_poss = np.random.choice(prob[loc],1,p=[0.75,0.25])
	else:
		move_poss = np.random.choice(prob[loc],1,p=pspace)
	if move_poss == ['*']: #The '*' character means movement only takes place within a set of problems of the same length as the current input problem
		st_locs = [i for i in range(len(loc))]
		val_loc = random.choice(st_locs)
		value = loc[val_loc]
		if value == '0':
			new_loc = loc[:val_loc] + '1' + loc[val_loc+1:]
		elif value == '1':
			new_loc = loc[:val_loc] + '0' + loc[val_loc+1:]
	if move_poss == ['+']: #The '+' character means movement only takes place within a set of problems of a longer length than the current input problem
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
	if move_poss == ['-']: #The '-' character means movement only takes place within a set of problems of a shorter length than the current input problem
		st_locs = [i for i in range(len(loc))]
		val_loc = random.choice(st_locs)
		value = loc[val_loc]
		new_loc = loc[:val_loc] + loc[val_loc+1:]
	return new_loc

def decision(agent,memory,problem):
	"""
	Calls the function for an agent to make a decision about whether or not to move to a new input problem

	Parameters
	----------
	agent : int
		The current agent.
	memory : dict
		key: agent
		value: solution [str]
	problem : str
		The current input problem.

	Returns
	-------
	[float]
		The normalized distance between an agent's current solution (memory[agent]) and their input problem (problem)
	"""
	sol_len = len(str(memory[agent]))
	prob_len = len(str(problem))
	return edit_distance(str(memory[agent]),str(problem))/max([sol_len,prob_len])