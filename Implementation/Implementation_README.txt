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
2.2.1.			Hashing
2.2.2.			Hash Map
2.2.3.			Sorting
2.3.			Merging
2.3.1.			Parameters
2.3.2.			Level >2 Merge
2.3.3.			Level 2 Merge
2.3.4.			Level 1 Merge

3.			Other Functions
3.1.			Gen
3.2.			Sample
3.3.			Search Space and Representations

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
Note that the purpose of this implementation to show that our attack works in practice and that our heuristics can be considered to be reasonable. Thus, there is significant room for improvement, since the fastest runtimes or most space efficient list management was never our intention. Nonetheless, we included some simple methods to make this attack feasible enough for small instances.


--- 2.1. PARAMETERS ---

- A, t, d, rf, Nw: see 1. Nomenclature
- max_iter: amount of unsuccessful iterations of the algorithm until it is aborded. By default set to 100000
- half: if s can be split into a left and right half, half can be set to true to only consider base lists where either the entire left half or the entire right half is constantly 0. Reduces runtime and success probability.


--- 2.2. LIST ORGANIZATION ---

- 2.2.1. HASHING -

To sort a vector into a bucket, we interpret it (or the result of a function f(v), e.g. A*v) as a q-adic number. This is done by the function assign_int(v, q). To reverse this, we call inv_assign_int(x, q, N), where denotes the length of the resulting vector in case of leading zeroes.

Note that assign_int(*,q) is injective for any search space that is a subset of Z_q^N, so assign_int can be utilized to filter remove multiples from a sorted list (see 2.2.3.).

To utilize Odlyzko's locality sensitive hashing function, call odlyzko(v, eta, q, give_c=False); the output is a binary interpretation of all possible odylzko hashes (i.e. the output is assign_int(h, 2) for all possible hash values h). If the binary odlyzko hash vector itself is required, set give_c=True.

As an example, for q=3329 and eta=1, the possible odlyzko hashes for v=(0,2,1664) are (0,0,0),(0,0,1),(1,0,0),(1,0,1), so odlyzko(v,eta,q) would return [0,1,4,5] (in some order).


- 2.2.2. HASH MAP -

To make the merging process easier, A level j list is comprised of a hash map L[* ,j] that maps any search space element v to either assing_int((A*v)[rf[j-1]:],q) or assing_int(g-(A*v)[rf[j-1]:],q), i.e. the last r[j-1] coordinates of A*v or g-A*v, respectively; here, g is the goal vector of the next level list. The hash buckets themselves are sorted lists that contain elements (v, A*v, assign_int(v,q)).


- 2.2.3. SORTING -

To reduce unnecessary memory consumption, lists are sorted on-the-fly into hash buckets that denote their potential collision candidates (see 2.2.). These buckets are comparatively small in expectation, so a combination of insertion sort combined with discarding multiples immediately ultimately is less memory consuming than leaving the buckets unsorted until the merge process is complete, where, in the worst case, only a relative 1/R[j] vectors remain after removing multiples (which is guaranteed to happen on level d-1).

Inserting a tuple x (concretely, the tuple (v, A*v, assign_int(v,q))) into a list L that is sorted by index i is done by calling L=insertion_bsearch(L, x, i). If the value from index i is already contained in the list, this routine returns L without modifying it.


--- 2.3. MERGING ---

In 2.2., we explained the data structure of our lists. Let us explain the merging process when given two level j lists L1=L[2i-1,j],L2=L[2i, j].


- 2.3.1. PARAMETERS -

- q, eta, t: see 1.1. and 1.2.
- L1, L2: lists to be merged
- nrf_next: N-rf[j-1], the last rf[j-1] coordinates that need to be matched
- Nw_next: Nw[j-1]
- sign, g: Lists are matched by finding v,w such that A*v=g-A*w for a fixed g; this can also be written as rf[j-1]*[0]+(-1)^0*A*v=g+(-1)^1*A*w, and the bucket can be picked with the hash of g+(-1)^sign*A*v for (g, sign)=(rf[j-1]*[0], 0) or (g, sign)=(g, 1)


- 2.3.2. LEVEL >2 MERGE -

Say list L1 contains buckets b[1],...,b[m] and L2 contains buckets c[1],...,c[n]. If b[y]=c[z], that means that, on the last rf[j-1] coordinates, A*v=g-A*w where g is the goal vector of L[i,j-1] and v,w are elements from b[y], c[z]. Thus, if v+w is in the level j-1 search space S, we can add v+w to L[i, j-1] (in the respective bucket with value assign_int(A*(v+w), q) or assign_int(g'-A*(v+w), q)). 

With this method and the hash map, we do not have to iterate over every list but can instead iterate over the hash buckets instead.

This merging routine is called with merge_lists(L1, L2, nrf_next, Nw_next, sign, g, q)


- 2.3.3. LEVEL 2 MERGE -

On level 1, we do not merge by matching some rf[0] coordinates; instead, we match approximately with the odlyzko hash function. Hence, we add v+w to the buckets assign_int(h,2) for all outputs of odlyzko(A*v, eta q) or odlyzko(t-A*v, eta q).

The level 2 merging routine is called with merge_lists_level_2(L1, L2, Nw_next, sign, g, q, eta).


- 2.3.4. LEVEL 1 MERGE -

On level 0, all we check for is whether A*s-t is small. Hence, we match the odlyzko buckets from L[1, 1] and L[2, 1] and check for this condition. In expectation, there is only one s that fulfills this condition.

This last merging process can be called upon with merge_lists_level_1(L1, L2, Nw_next, t, q, eta).






---------- 3. OTHER FUNCTIONS ----------

Overall, our contribution is described and contained in 2. . In this section, we only present a couple of inclusions that are not novel but helpful when analyzing the algorithm.


--- 3.1. GEN ---

Gen(N, eta, q, rf_1, pk_only=False) creates an LWE key pair. The dimension ist N, the underlying modulus is q and the private keys are sampled according to B(eta). rf_1 denotes the amount of coordinates of e that are artificially set to 0 (to make the algorithm easier). if pk_only is set to True, this returns the public key only.


--- 3.2. SAMPLE ---

matsample(q,m,n), vecsample(q,m), GFsample(q): draws a uniformly sampled matrix of dimension m*n(matsample), a vector of dimension n (vecsample) or an element (GFsample) mod q.

create_vec(Nw_j, q, shuffling=False) returns a vector from the core set of Nw_j; if shuffling=True, this will be a random vector, otherwise the returned vector will always be the same.


--- 3.3. SEARCH SPACE AND REPRESENTATIONS ---

searchspace(Nw_j) returns the size of search space Nw_j.

representations(Nw_next, eps) calculates, given the next level search space distirbution Nw_next and the current level epsilon parameter set eps, the amount of representations a single vector for level j-1 as the sum of two level j vectors has.

level_descriptions(Nw, eps) returns the above numeric properties for all search space distributions Nw.














---------- GLOSSARY ----------

A									1.2.
assign_int						2.2.1.
avg_L								1.3.

create_vec						3.2.

d									1.1.

e									1.2.
eta								1.1.

g									1.3.
Gen								3.1.
GFsample							3.2.

insertion_bsearch			2.2.3.
inv_assign_int					2.2.1.

k									1.4.

L									1.3.
level_description			3.3.

matsample						3.2.
Meet								2.
merge_lists						2.3.2
merge_lists_level_1			2.3.4
merge_lists_level_2			2.3.3


N									1.1.
Nw									1.1.

odlyzko							2.2.1.

q									1.1.

R									1.4.
representations				3.3.
rf									1.4.
rfloor							1.4.

s									1.2.
S									1.4.
searchspace						3.3.

t									1.2.
tq									1.3.

vecsample						3.2.

