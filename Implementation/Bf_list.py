from IPython.display import clear_output
from sympy.utilities.iterables import multiset_permutations

from Sort_search import assign_int

def brute_force_list(
    A,
    Nw,
    g_next,
    g,
    sign,
    q
):
    N=len(create_vec(Nw,q))
    negr=N-len(g)
    negg=len(g_next)-len(g)
    negr_next=N-len(g_next)
    out={}
    counter=0
    for v in multiset_permutations(create_vec(Nw,q)):
        counter+=1
        if counter%1000==0:
            clear_output(wait=True)
            print(counter)
        v=array(v)
        Av=A@v
        if list((Av)[negr:])==list(g):
            assint=assign_int(g_next+(-1)**sign*(Av)[negr_next:],q)
            if assint in out:
                out[assint]+=[(v,Av, assign_int(v,q))]
            else:
                out[assint]=[(v,Av, assign_int(v,q))]
    return out
            
            