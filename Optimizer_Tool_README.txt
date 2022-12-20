---------- README ----------

This readme provides a thorough explanation for both the optimization tool as well as the evaluation tool.

Organization of this file:

1. 			Search Spaces, Distributions and Entropy
1.1.			Search Spaces
1.2.			Distributions
1.3. 			Entropy

2.			Specific Distributions
2.1.			CBD
2.2.			Uniform Distributions
2.3.			Ternary Distributions
2.4.			BLISS Distributions

3.			Rep Parameters
3.1.			eps
3.2.			eps functions
3.2.1.				nulleps
3.2.2.				leveleps
3.2.3.				copyeps
3.2.4.				formateps
3.3.			Evaluation

4.			optimizer
4.1.			Parameters
4.2.			Phase 1: setup
4.2.1.				In a Nutshell
4.2.2.				Parameters
4.2.3.				setup
4.3.			Phase 2: Discrete Gradient Descent (gd_search)
4.3.1.				In a Nutshell
4.3.2.				Parameters
4.3.3.				gd_search

5.			Optimizing the optimizer
5.1.			No immediate Reverts
5.2.			No minimal Improvements
5.3.			Parameter subsets
5.3.1.				create_randset
5.3.2.				fullbintruthdict
5.4.			Subroutine: lightning_gd
5.4.1.				In a Nutshell
5.4.2.				Parameters
5.4.3.				Motivation

6.			Printing LaTeX compilable tables
6.1.				Parameters

			Glossary






---------- 1. SEARCH SPACES, DISTRIBUTIONS AND ENTROPY ----------


--- 1.1. SEARCH SPACES ---

Search space distributions are denoted with arrays w=[w[0],w[1],w[2],...,w[max(4,eta)]] of length >=5 where w[i] denotes the relative amount of i in every vector s in S.
We will denote search space distributions with search spaces from here on.


--- 1.2. DISTRIBUTIONS ---

If a probability distribution is symmetrical around 0, we use its equivalent search space notation w instead. Otherwise, we use the variable p=[p[0],...,p[k]].


--- 1.3. ENTROPY ---

To calculate the entropy of ANY distribution p, call quentropy(p,1). If the distribution is not normalized, call quentropy(p,scale) instead, where every p[i] is scaled down according to scale.
In rare cases, quentropy behaves weird, i.e. when sum(p) is not 1 due to rounding errors; to avoid these rounding errors, set incomplete=False.

To calculate the entropy of a search space, it is instead sufficient to call searchspace(w) instead. This function automatically counts w[i] twice for each i>0.




---------- 2. SPECIFIC DISTRIBUTIONS ----------


--- 2.1. CBD ---

To call the probability function, call pbin(eta, i).
To create a search space distributed according to the CBD, call centered_binom_search(eta) or etaSearch(eta).


--- 2.2. UNIFORM DISTRIBUTIONS ---

To create a search space distributed according to the uniform distribution, call uniSearch(eta).


--- 2.3. TERNARY DISTRIBUTIONS ---

To create a search space distributed according to T(weight)=[1-2*weight,weight,0,0,0], call terSearch(weight).


--- 2.4. BLISS DISTRIBUTIONS ---

To create a search space distributed according to BLISS' search spaces, call Blissdist[k] where k corresponds to the numbering of the specific distribution (e.g. to call for BLISS-IV, call Blissdist[4]).




---------- 3. REP PARAMETERS ----------


--- 3.1. EPS ---

Optimization parameters are stored in dictionaries, throughout the program referred to as "eps".
One parameter can be called upon with both its representation index as well as its corresponding level, e.g. to call the parameter epsilon_10 of level 6, call name_of_eps[10,6].
A parameter set for a depth d tree contains exactly 8*(d-1) parameters eps[i,j]; if another representation method than Rep-3 is used, the corresponding eps entries are not to be considered during optimization and have to remain 0 (e.g. when optimization for Rep-2, we have eps[30,j]=eps[31,j]=eps[32,j]=eps[33,j]=0 for every j).

The parameter sets we found for predefined distributions can be called as follows:
- for CBD parameters (B(eta)), call binomialeps[eta, d] (Rep-3) or binomialeps_rep2[eta, d] (Rep-2)
	- 1<=eta<=3,
	- 1<=d<=8
- for uniform parameters (U(eta)), call uniformeps[eta, d]
	- 1<=eta<=3,
	- 1<=d<=8
- for ternary distributions (T(omega)), call ternaryeps[omega, d]
	- omega={0.3, 0.375, 0.441, 0.5, 0.62, 0.667},
	- 1<=d<=8
- for BLISS distributions, call blisseps[k, d] (e.g. for BLISS-IV, k=4)
	- 0<=k<=4,
	- 1<=d<=8


--- 3.2. PARAMETER EPS FUNCTIONS ---

We provide some functions to create and modify epss. These are as follows:


- 3.2.1. NULLEPS -

nulleps(d) returns a eps of depth d that only contains 0 entries for every parameter.


- 3.2.2. LEVELEPS -

leveleps(eps, j) returns all 8 parameters of the designated level j in form of an array [eps[10,j],eps[20,j],eps[21,j],eps[22,j],eps[30,j],eps[31,j],eps[32,j],eps[33,j]].


- 3.2.3. COPYEPS -

copyeps(eps) creates another eps with the same entries as eps.
Can also be used to merge 2 epss. For this, set three additional optional parameters epsscale, changeeps and changescale. The output will then be of the form output[i,j]=eps[i,j]*epsscale+changeeps[i,j]*changescale


- 3.2.4. FORMATEPS -

formateps(eps,d) returns an output eps of depth d where output[i,j]=eps[i,j] if the latter is defined and 0 otherwise.
Optionally, the order of the output eps can be sorted by ascending level first, representation index second (set levelfirst=True) or descending level first, representation index second (set reverselevelfirst=True).


--- 3.3. EVALUATION ---

To find the amount of representations (in log_(2^N)) that exist for a search space w and a set of parameters [eps[10],...,eps[33]], call representations(w, [eps[10],...,eps[33]])

To evaluate runtime and list size of a distribution dist and a given parameter set eps, call evl(dist, d, eps) where d is the depth of the tree. This returns two arrays of depth d+1, where
- the first array T contains the run times T[j] it takes to build the level j list and
- the second array L contains level j list sizes L[j].
Both T[j] and L[j] will be logarithmic with base 2^N.

To only return T, call evl(dist, d, eps, retL=False) or evl_T(dist, d, eps). Similarly, returning only L is achieved by evl(dist, d, eps, retT=False) or evl_L(dist, d, eps).

Both representation and evaluation functions take their expression from the paper.




---------- 4. THE OPTIMIZER ----------

The actual optimization consists of a Brute Force initialization, called Setup, and a greedy and discrete version of gradient descent, called gd. Both functions Setup() and gd_search() are recursive functions, where each function call only looks to optimize the parameters of the current level.
To optimize a distribution dist for depth d=4, call optimizer(dist, d=4, rough=10, gamma=0.001, delta=0.0001, setupdelta=0.001, gd_delta=0, gd_scale=1, gd_round=True, initeps={}, f=ideps, lightningiter=1000000, optruthdict={}, printset=[]). dist is the only mandatory input required, but it is highly recommended to alter a significant amount of optional arguments to reduce run time significantly.

The second phase, gd_search, is called iteratively, until a runtime improvement would be too small to encourage further optimization efforts. In numbers, given some delta>=0, this implies that, to iterate through gd_search again, we require our runtime improvement to be greater than delta.


--- 4.1. PARAMETERS ---

- dist: distribution for which we hope to find a good parameter set
- d: search tree depth. By default set to 4
- rough, setupdelta: see 4.2.2.
- gamma, gd_delta, gd_scale: see 4.3.2.
- delta: dictates the minimal runtime improvements that need to be made to stop algorithm from terminating. By default set to 0.0001 .
- gd_round: If set to False, omits any gd_search and outputs the parameter set found after phase 1. By default set to True.
- initeps: initeps describes the parameter set that we want to optimize. By default set to {}. If initeps is left as {}, the optimizer will find a decent parameter set to initiate the optimizing process from; otherwise, the setup phase will be skipped and initeps will be used as starting point for the gd_search phase.
- f: f can be set to either roundeps or ideps. If set to roundeps, every parameter set found by setup and gd_search will be rounded to 3 decimal places. By default set to ideps
- lightningiter: see 5.4.2.
- optruthdict: see 5.3.
- printset: every time either setup or gd_search finds a new parameter eps that improves optT, every element inside printset is printed. Only interesting on multiple iterations of the optimization program. By default, printset is empty (Note that opteps, T and optT are always printed when optT decreases, independently of printset).


--- 4.2. PHASE 1: SETUP ---

The first phase is called with Setup(w, R, S, T, L, d, curlevel, optT, opteps, initeps, rough=4, setupdelta=0.0001, printset=[]), where the last 3 arguments are optional and remain unchanged throughout each recursive step.


- 4.2.1. IN A NUTSHELL -

The setup phase does not aim to find an optimal parameter; instead, it aims to find a good starting point by finding the best parameter set where every parameter is a multiple of some comparatively large number, e.g. 0.1 or 0.25 . This search is entirely conducted through brute force.


- 4.2.2. PARAMETERS -

- w: Array that contains d+1 distribution arrays, each distribution w[j] describes the search space distribution on level j; for j>curlevel, w[j] is constantly set to [0,...,0].
- R: Array that contains d+1 numbers, denoting the amount (in log_(2^N)) of representations R[j] found on level j with the current parameter set; for j>curlevel, R[j] is constantly set to 0.
- S: Array that contains d+1 numbers, denoting the search space size S[j] (in log_(2^N)) of w[j] on level j with the current parameter set; for j>curlevel, S[j] is constantly set to 0.
- T: Array that contains d+1 numbers, denoting the run time T[j] (in log_(2^N)) required to build one level j list; for j>curlevel, T[j] is constantly set to 0.
- L: Array that contains d+1 numbers, denoting the memory requirements L[j] (in log_(2^N)) for one level j list; for j>curlevel, L[j] is constantly set to 0.
- d: Meet-LWE tree depth.
- curlevel: current level in which parameters are to be optimized.
- optT: describes the currently best known runtime for any parameter set. Is to be optimized.
- opteps: describes a parameter eps that would yield the currently best known runtime, i.e. optT=max(evl_T(dist, d, opteps)).
- initeps: propagates the lower level parameters to the current level. If, on curlevel=d-1, we have optT>evl_T(dist, d, initeps), we update opteps to initeps. When this readme mentions the "current parameter set", initeps is what that refers to.
- rough: Brute Force step size: For every eps[i,j] where i={10, 20, 21, 22, 30, 31, 32, 33}, 1<=j<d, we try exactly rough+1 many parameters in the setup phase. By default set to 4.
- setupdelta: Reduces runtime in exchange for thoroughness: To consider the current initeps, we are required to improve the runtime by at least setupdelta, i.e. max(evl_T(dist, d, initeps))-optT>setupdelta. By default set to 0.0001 .
- printset: every time Setup finds a new parameter eps that improves optT, every element inside printset is printed. Only interesting on multiple iterations of the optimization program. By default, printset is empty (Note that opteps, T and optT are always printed when optT decreases, independently of printset).


- 4.2.3. ALGORITHM -

The setup phase only takes place if the optimal argument initeps has not been altered; otherwise, the setup phase will be skipped and the gd_search phase will be immediately initiated.

initeps can be considered as this routine's working parameter set. For every initeps[i,j], setup cycles through all multiples of 1/rough and evaluates the runtime with these parameters. When the current parameter set improves the runtime, it replaces the former best known parameter set (called opteps) as the new optimal parameter set.

setup is a recursive routine. Its inputs contain values d and curlevel, where initially, curlevel=1. If an appropriate set of parameters eps[i, curlevel] for the current level have been found, Setup will be called again with curlevel+1, so the parameters of the current level can be propagated one level down. Parameters are considered appropriate in this sense when 
- they don't increase the runtime (i.e. T[curlevel-1]>optT) and
- the parameters don't try to represent more values than exist on level curlevel-1 (e.g. there are relative 0.1 entries 1 on level curlevel-1, but eps[10,curlevel]=0.2 would try to represent relative 0.2 entries 1, which is more than there are in the first place).
When curlevel=d-1, instead of calling setup again, the program instead evaluates the final runtime. If it improves on the current optimal runtime, initeps replaces the old best parameter set opteps.

To improve the runtime of the setup phase, appropriate values for rough and setupdelta can be set:
- increasing rough means that more possible values for initeps[i,j] will be considered. Worst case is that all (rough+1)^(8*(d-1)) parameters come into consideration, which is infeasible to optimize even with moderate tree depths.
- setupdelta demands that, in order to take a parameter set into consideration, it needs to improve the best known runtime by at least setupdelta. Therefore, runtime can be improved by setting an appropriate value for setupdelta, say 0.0001.

The argument printset does not impact optimization and is only of interest when optimizing multiple distributions at once or the same distribution with multiple iterations, e.g. when optimizing different parameters each time.


--- 4.3. PHASE 2: DISCRETE GRADIENT DESCENT (GD) ---

The second and arguably more important phase is called with gd_search(w, R, S, T, L, dist, d, curlevel, optT, opteps, oldeps, oldchangeeps, initeps, changeeps, optchangeeps, gamma=0.001, gd_delta=0, gd_scale=1, lightningiter=100000, printset=[]), where the last 5 arguments are optional and remain unchanged throughout each recursive step.


- 4.3.1. IN A NUTSHELL -

gd_search is called iteratively by the optimizer function. Each time it is called, it looks for the best parameter set in the immediate vicinity of the current best parameter set called oldeps.

gd_search can be considered a discrete version of the gradient descent optimization for a non-differentiable function.


- 4.3.2. PARAMETERS -

- w, R, S, T, L, d, curlevel, optT, opteps, initeps, printset: same functionality as with setup.
- oldeps: contains the output from the previous iteration of gd_search (or the output of setup/initial input initeps, if this is the first call of gd_search).
- oldchangeeps: contains the optchangeeps from the previous iteration of gd_search (or nulleps(d-1), if this is the first call of gd_search).
- changeeps: contains the changes made to all parameters in initeps, compared to oldeps (i.e. changeeps=oldeps-initeps).
- optchangeeps: contains the changes made to the optimal parameter set from the previous iteration, compared to oldeps.
- gamma: denotes the search step size, i.e. initeps[i,j]-oldeps[i,j] is always k*gamma for some integer k. Initially set to 0.001.
- gd_delta: similar functionality to setupdelta, i.e. we want to improve the runtime by at least gd_delta in each step. Initially set to 0.
- gd_scale: similarly to gd_delta, gd_scale dictates a minimal improvement over optT by scaling it by a relative amount. Overall formula is max(T[0],...,T[curlevel-1])<gd_scale*optT-gd_delta. initially set to 1.
- lightningiter: dictates an upper bound of parameters that are to be looked at in the lightning_gd phase, i.e. the runtime of one iteration of lightning_gd (see 5.4.). Initially set to 1000000.


- 4.3.3. GD_SEARCH -

The underlying idea of gd_search stems from a regular gradient descent optimization: from the currently best known parameter set, locate the direction of the steepest descent and take an appropriate step size in that direction to find a slightly better set of parameters. Repeat from there until either the minimum has been found or the difference in function values becomes too small to matter.

Unfortunately, the function we want to minimize (optT) is not differentiable everywhere since optT=max(T[j]). Additionally, experiments let us believe that, for an optimal parameter set eps, there is a k>1 such that T[1]~...~T[k], so we have no hope to be working on any differentiable subset of all parameters.

Instead, what we do is to consider all parameters as a grid of step size gamma: denote oldeps as the output from the previous iteration of gd_search. Then, consider all parameter sets eps where eps[i,j] is contained in the set {oldeps[i,j]-gamma, oldeps[i,j], oldeps[i,j]+gamma}. Out of all these, pick the parameter set that yields the best results, and start over. Eventually, we should find a local minimum and abort the algorithm.




---------- 5. OPTIMIZING THE OPTIMIZER ----------

In the state described above, gd_search would consider O(3^((d-1)*8) ) many parameter sets per iteration: We have 8 parameters per level and there are parameters on every level j=1,...,d-1. As a result, this method is rendered inconceivable for even moderate tree depths.

To combat these runtimes, we introduced methods to reduce the overall runtime significantly. These changes reduce the runtime significantly, so that it is now possible to find parameter sets with a decent value optT within only a few minutes.


--- 5.1. NO IMMEDIATE REVERTS ---

oldchangeeps remembers which parameters were changed in the previous iteration. In the current iteration, these parameters will not be considered for change in the opposite direction. For example, if eps[10,1] was changed from x to (x+gamma) in the previous iteration, in the current iteration, gd_search would only consider parameter sets where eps[10,1] were either (x+gamma) or (x+gamma)+gamma, dismissing (x+gamma)-gamma. This makes it impossible to immediately revert changes from the previous iteration.


--- 5.2. NO MINIMAL IMPROVEMENTS ---

gd_delta and gd_scale demand that a minimal runtime improvement needs to be made, so parameters where the improvement is considered to be too miniscule will be dismissed regardless of whether they improve optT or not.


--- 5.3. PARAMETER SUBSETS ---

Instead of optimizing all 8*(d-1) many parameters in one singular iteration of optimizer, we randomly choose, say, k parameters per level (so k*(d-1) many parameters overall) and only optimize these parameters while leaving the parameter values for the other (8-k)*(d-1) parameters unchanged. Naturally, most parameters directly or indirectly interact with each other in terms of runtimes, so limiting the optimization process only to a handful of parameters almost certainly yields the drawback that this method would not produce the optimal parameter set - even after multiple iterations, each with randomly drawn parameters to optimizte. However, we assume the difference in the optimal runtime compared to our runtime to be too small to be of serious interest.

Whether a parameter eps[i,j] is to be optimized in a current iteration is determined by a so called truth dictionary, called truthdict: a truthdict td should be comprised of boolean entries td[i,j] where parameter eps[i,j] should be considered for optimization if and only if td[i,j] is set to True. Creating such truth dictionaries can be done by randomly sampling binary strings of length 8*(d-1).


- 5.3.1. CREATE_RANDSET -

create_randset(d) creates 300 bitstrings. Each string is comprised of d substrings of length 8, where each substring has a predefined hamming weigth: the first 100 bitstrings have substring hamming weight 2, the next 100 have hamming weight 3 and the last 100 strings have hamming weight 4.

If bitstrings of different hamming weight should also be included or the amount of weight 2, 3, 4 strings should be altered, use optional arguments it1, it2, etc. . For example, to add 500 additional bitstrings of substring hamming weight 5, use it5=500.


- 5.3.2. FULLBINTRUTHDICT -

These bitstrings can be used to create a truth dictionary. For example, the string '11110000' denotes that the first 4 parameters (dict[10,j], dict[20,j], dict[21,j], dict[22,j]) are set to true, while the last 4 parameters (dict[30,j], dict[31,j], dict[32,j], epdicts[33,j]) will remain constant throughout this iteration of optimizer.

To convert a string s to a truthdict, call fullbintruthdict(s).

If given a randset comprised of binary strings of length 8*(d-1), it is easy to convert them to truthdicts and iterate the optimizer over all truthdicts to find a suitably good parameter set.

In one iteration of optimizer, the global value gd_set denotes which parameters are to be optimized in the corrent optimization iteration: gd_set[i,j] either is equal to [0] or to [-gamma,0,gamma] depending on whether optruthdict[i,j] is set to False or True.


--- 5.4. SUBROUTINE: LIGHTNING_GD ---

Finally, after finding a paramter set that improves optT, instead of looking at all other neighbors of oldeps to maybe improve even more, we interject with one iteration of lightning_gd, a subroutine that only considers parameters in the current set changeeps (the set of parameters that have changed compared to oldeps).

Optionally, every time gd_search finds a better parameter set, subroutine lightning_gd(w, R, S, T, L, d, curlevel, optT, opteps, oldeps, initeps, changeeps, optchangeeps, lightningsets, gamma=0.001, printset=[]) may be triggered. lightning_gd contains 2 optional, unchanging arguments.


- 5.4.1. IN A NUTSHELL -

After finding a parameter set with gd_search that yields better runtimes that optT, lightning_gd continues searching for better parameter in the direction the changed parameters are pointing. lightning_gd only considers parameters that differ from their oldeps counterparts.


- 5.4.2. PARAMETERS -

- w, R, S, T, L, d, curlevel, optT, opteps, oldeps, initeps, changeeps, optchangeeps, gamma, printset: same functionality as with gd_search.
- lightningsets: Upper bounds the amount of parameter sets that are to be considered in one coll of lightning_gd. By default set to 1000000.


- 5.4.3. MOTIVATION -

In the lightning subroutine, we want to inspect the region in which all changing parameters are pointing. Say, for example, we find a parameter set initeps that shows an improved runtime over oldeps while only 3 parameters change: initeps[10,1], initeps[10,2], initeps[10,3]. That means that changeeps[i,j]=0 for all [i,j]!=[10,1],[10,2],[10,3]. Also, changeeps[i,j]=gamma or -gamma for [i,j]=[10,1],[10,2],[10,3].

We consider it reasonable to assume that, for multiples of changeeps[10,1], changeeps[10,2], changeeps[10,3], there is a good chance that a change of 2*changeeps[10,1], 2*changeeps[10,2], 2*changeeps[10,3] could yield even better results, and maybe 3*changeeps[10,1], 3*changeeps[10,2], 3*changeeps[10,3] would improve the runtime again. However, to find that out under normal circumstances, we would have to cycle through two iterations of gd_search, which can cost a lot of time, depending on the parameter subset which we are improving right now.

Instead, what we can do is the following: Consider every changeeps[10,1] times some factor s[10,1], combined with every multiple s[10,2] of changeeps[10,2] and every multiple s[10,3] of changeeps[10,3]. If we upper bound the factors s[10,1], s[10,2], s[10,3] by some absolute value scale, we only have to look at O(scale^3) many combinations - with a decent chance of finding a significantly improved new parameter set.

Now, say that we have k parameters that change, going from oldeps to initeps. In that case, we have to look at O(scale^k) many parameter combinations instead. Hence, if we want to do at most lightningiter many iterations, choosing scale=floor(lightningiter^(1/k)) lets us do exactly that.

After <=lightningiter many iterations, the optimal parameter set found will be returned, and gd_search continues as usual.




---------- 6. TABLEPRINT ----------

It is possible to print tables containing all parameters and runtimes, similar to the tables at the end of our paper. To do so, include the packages tabular, hhline, xcolor, colortbl, in the preamble. Additionally, define the colow \definecolor{Gray}{gray}{0.9}.

To print a singular table for one distribution dist and one parameter set eps, call Tableprint(name, eps, eta=3, d=4, dist=[], treatzero=" ", ifthrees=True, ifcolor=True, iftop=False, ifbottom=False).


--- 6.1. PARAMETERS ---

- name: Puts the given name in the leftmost column of the table.
- eps: parameter set to be printed.
- eta: if dist is undefined, the distribution will be set to centered_binom_search(eta) by default. Set to 3 by default.
- d: denotes the depth of the search tree and the table. By default set to 4.
- dist: Distribution to be displayed in the table. If left [], automatically assumes that the distribution is centered_binom_search(eta).
- treatzero: Denotes how zeroes will be displayed in the table. By default set to " ".
- ifthrees: If True, parameters eps[30,j], eps[31,j], eps[32,j], eps[33,j] will be displayed in the table. Set to False if parameters are Rep-2 parameters only.
- ifcolor: If True, every second column will be gray. By default set to True.
- iftop, ifbottom: These two boolean values denote whether or not the top and bottom of the table will be printed. If multiple epsilon parameter sets are to be displayed, it is recommended to set both to false and print the top and bottom separately.











---------- GLOSSARY ----------

binomialeps						3.1.
blisseps							2.4., 3.1.
Blissdist						2.4.

centered_binom_search		2.1.
copyeps							3.2.3.
counteps							x.y.3.
create_randset					5.3.1.

etaSearch						2.1.
evl								3.3.
evl_T								3.3.
evl_L								3.3.

formateps						3.2.4.
fullbintruthdict				5.3.2.

ideps								4.1.
initeps							4.2., 4.3.

leveleps							3.2.2.
lightning_gd					5.4.

nulleps							3.2.1.

optimizer						4.
optruthdict						5.3.2.

pbin								2.1.

representations				3.3.
roundeps							4.1.

searchspace						1.3.
setup								4.2.

tableprint						6.
ternaryeps						3.1.
terSearch						2.3.

uniformeps						3.1.
uniSearch						2.2.

quentropy						1.3.