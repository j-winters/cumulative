import numpy as np
import editdistance

def entropy(string):
	"""
	Calls the function to calculate entropy (in bits) of a string.

	Parameters
	----------
	string : str
		A binary string of n-length, e.g., '01011'

	Returns
	-------
	[float]
		An entropy value between 0.0 and 1.0 bit.
	"""
	prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
	return - sum([ p * np.log(p) / np.log(2.0) for p in prob ])

def edit_distance(s1, s2):
	"""
	Calls the function to calculate the edit distance betwee two strings.

	Parameters
	----------
	s1 : str
		A binary string of n-length, e.g., '01011'
	s2 : str
		A binary string of n-length, e.g., '01011'

	Returns
	-------
	[float]
		Levenshtein edit distance between two strings.
	"""
	return editdistance.eval(s1, s2)

def string_complexity(string):
	"""
	Calls the function to calculate the complexity of the string.

	Parameters
	----------
	string : str
		A binary string of n-length, e.g., '01011'

	Returns
	-------
	[float]
		Entropy value multiplied by the length of the string.
	"""
	return entropy(string) * len(string)