---------- README ----------

This readme provides a thorough explanation for our implementation of our attack.

Organization of this file:

1. 		Nomenclature
1.1.			Parameters
1.2.			Keys
1.2.			Algorithm
1.2.			Other

2. 		Algorithm
2.1.			Parameters
2.2.			List Organization
2.2.1.			Sorting
2.2.2.			Hashing

			Glossary






---------- 1. NOMENCLATURE ----------


--- 1.1. PARAMETERS ---

- q (int): modulus for the finite field F_q
- N (int): matrix and vector dimension
- d (int): Algorithm tree depth
- Nw (array): contains d+1 arrays with integers; Nw[j] describes the distribution of level j search space S, i.e. Nw[j][i] denotes the amount of times a vector v in S contains the entry i (and -i)
- eta (int): secret key sampling parameter
- rf/rfloor (array): contains d+1 integers; r[j] denotes the amount of integers to be fixed in a single level, i.e. the dimension of an intermediate goal vector g


--- 1.2. KEYS ---

- A (array matrix): uniformly sampled public key matrix of dimension N*N
- s (array): randomly sampled secret key vector of dimension N; sampled according to centered binomial distribution with parameter eta; is element from S[0] by design
- e (array): randomly sampled secret key vector of dimension N; sampled according to binomial distribution with parameter eta; by design, last rf[1] entries are 0
- t (array): public key vector of dimension N; satisfies t=A*s+e


--- 1.3. ALGORITHM ---

- L (dict): contains 1+2+4+8+...+2**d search tree lists L[i,j] of vectors
- g (dict): contains 2+4+8+...+2**(d-1) vectors of dimension rf[1], rf[2], ... ,rf[d-1]; g[i,j] denotes the intermediate requirement of list L[i,j], i.e. all vectors v in L[i,j] satisfy A*v being equal to g[i,j] in the last r[j] coordinates
- tq(dict): contains 1+2+4+...+2**(d-2) uniformly sampled vectors of dimension rf[1], rf[2], ... ,rf[d-1]; denotes the intermediate merge targets
- avg_L (array): contains d+1 arrays; avg_L[j] contains the list size of every level j list found in any iteration of the algorithm


--- 1.4. OTHER ---

- k (GF): finite field over modulus q
- R (array): contains d+1 integers; R[j] denotes the amount of representations for a vector from level j-1 search space with two level j vectors; satisfies log_q(R[j])~rf[j]
- S (array): contains d+1 integers; S[j] denotes the size of level j searchspace S






---------- 2. ALGORITHM ----------


The attack itself is called upon with Meet(A, t, d, rf, Nw, max_iter=100000, half=False), where the last 2 arguments are optional.
Note that the purpose of this implementation to show that our attack works in practice and that our heuristics can be considered to be reasonable. Thus, there is significant room for improvement, since fast runtimes or space efficient list management was never our intention. 


--- 2.1. PARAMETERS ---

- A, t, d, rf, Nw: see 1. Nomenclature
- max_iter: amount of unsuccessful iterations of the algorithm until it is aborded. By default set to 100000
- half: if s can be split into a left and right half, half can be set to true to only consider base lists where either the entire left half or the entire right half is constantly 0. Reduces runtime and success probability.


--- 2.2. LIST ORGANIZATION ---


- 2.2.1. SORTING -

To reduce unnecessary memory consumption, lists are sorted on-the-fly into hash buckets that denote their potential collision candidates. These buckets camparatively small in expectation, so a combination of insertion sort combined with discarding multiples immediately ultimately is less memory consuming than leaving the buckets unsorted until the merge process is complete, where, in the worst case, only a relative 1/R[j] vectors remain after removing multiples.


- 2.2.2. HASHING -

To sort a vector into a bucket, we interpret it (or the result of a function f(v), e.g. A*v) as a q-adic number. This is done by the function assign_int(v, q). To reverse this, we call inv_assign_int(x, q, N), where denotes the length of the resulting vector in case of leading zeroes.

To utilize Odlyzko's locality sensitive hashing function, call odlyzko(v, eta, q, give_c=False); the output is a binary interpretation of all possible odylzko hashes. If the binary odlyzko hash vector itself is required, set give_c=True.


(tbc)









---------- GLOSSARY ----------

A									1.2.
assign_int						2.2.2.
avg_L								1.3.

d									1.1.

e									1.2.

eta								1.1.

g									1.3.

inv_assign_int					2.2.2.

k									1.4.

L									1.3.

Meet								2.

N									1.1.
Nw									1.1.

q									1.1.

R									1.4.
rf									1.4.
rfloor							1.4.

s									1.2.
S									1.4.

t									1.2.
tq									1.3.

