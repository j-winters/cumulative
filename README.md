# cumulative
This repository contains data and code from Winters (2019). It includes the Python code used for running the model, the data generated for Winters (2019), and the R code used to analyse this data.

The top-level folder structure is as follows:

* `analysis/`: Contains R code for producing all graphs in the paper.
* `data/`:  All data generated for Winters (2019) in `.csv` formats.
* `manuscript/`: Pre-print pdf.
* `model/`: The ABM used for generating the data. Requires Python 3 with [NumPy](https://numpy.org/), [NetworkX](https://networkx.github.io/) and [Editdistance](https://github.com/aflc/editdistance) packages installed.

## Running the model
The actual simulation runs reported in the paper were parallelized using the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) package. I have also created a brief tutorial at the following [NextJournal notebook](https://nextjournal.com).

Below is a simple version of the model for performing a single run:
```python
>>> import ABM *
>>> simulation(n=100,generations=100,trans_param=1.0,optimization=0.6,exploration=0.2,directory='output.txt',run=0,out='False',pspace=[0.5,0.3,0.2])
```

If `out=True`, a single simulation will run and output the `.txt` specificed using the `directory` parameter, else if `out=False` then the output will print in your console. There are several additional parameters that can be manipulated and these are detailed below:

* `n`: Number of agents in a population.
* `generations`: Number of generations for a given run.
* `trans_param`: Proportion with which agents receive a transmitted solution from another agent in the population. The default is `trans_param=1.0` and corresponds to agents who always receive a transmitted solution. When `trans_param=0.0`, agents never receive a transmitted solution.
* `optimization`: Proportion with which agents choices are biased or stochastic. The default is `optimization=0.6` and corresponds to agents who only select the most optimized variant 60% of the time. 
* `exploration`: The threshold at which agents consider moving to a novel problem in the problem space. If `exploration=0.2` (the default) then agents move when a solution-problem mapping has a normalized Levenshtein distance < 0.2.
* `pspace`: This is the probability with which an agent considers movement to problem where its length is the same, longer, or shorter. The default is `pspace=[0.5,0.3,0.2]`: P(Same)=0.5, P(Longer)=0.3, P(Shorter)=0.2.

## References
Winters, J. (2019). Escaping optimization traps: The role of cultural adaptation and cultural exaptation in facilitating open-ended cumulative dynamics. *Palgrave Communications*, XXXX.

License
-------

Except where otherwise noted, this repository is licensed under a Creative Commons Attribution 4.0 license. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit, provide a link to the license, and indicate if changes were made. See LICENSE.md for full details.
