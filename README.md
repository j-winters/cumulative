# cumulative
This repository contains data and code from Winters (2019). It includes the Python code used for running the model, the data generated for Winters (2019), and the R code used to analyse this data. 

The top-level folder structure is as follows:

* `model/`: The ABM used for generating the data. Requires Python 3 with [NumPy](https://numpy.org/), [NetworkX](https://networkx.github.io/) and [Editdistance](https://github.com/aflc/editdistance) packages installed.
* `data/`:  All data generated for Winters (2019) both in the raw `.txt` and curated `.csv` formats.
* `analysis/`: Contains R code for producing all graphs in the paper.

## Running the model
There are two ways to run the model. The first is to run a simple model as follows:
```python
>>> import ABM_palgrave *
>>> probs = {'00':['*','+'],'01':['*','+'],'10':['*','+'],'11':['*','+']}
>>> simulation(prob=probs,n=100,generations=100,invent_param=1.0,del_param=1.0,mod_param=1.0,trans_param=1.0,optimization=0.6,exploration=0.2,directory='output.txt',run=0,start_pos=2)
```

This performs a single simulation run which outputs the `.txt` specificed using the `directory` parameter. There are several parameters that can be manipulated and these are detailed below:

* `n`: Number of agents in a population.
* `generations`: Number of generations for a given run.
* `trans_param`: Proportion with which agents receive a transmitted solution from another agent in the population. The default is `trans_param=1.0` and corresponds to agents who always receive a transmitted solution. When `trans_param=0.0`, agents never receive a transmitted solution.
* `optimization`: Proportion with which agents choices are biased or stochastic. The default is `optimization=0.6` and corresponds to agents who only select the most optimized variant 60% of the time. 
* `exploration`: 

## References
Winters, J. (2019). Escaping optimization traps: The role of cultural adaptation and cultural exaptation in facilitating open-ended cumulative dynamics. Palgrave Communications, XXXX.

License
-------

Except where otherwise noted, this repository is licensed under a Creative Commons Attribution 4.0 license. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit, provide a link to the license, and indicate if changes were made. See LICENSE.md for full details.
