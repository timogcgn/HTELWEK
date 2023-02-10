from Sort_search import assign_int, insertion_bsearch
from Odlyzko import odlyzko, eta_small
from Sampling import inv_create_vec
from Lists import weight
import gc

def merge_lists(L1, L2, rf_x, nrf_x, Nw_prevlevel, sign, g, q):
    out={}
    for key in L1:
        if key in L2:
            for vec1 in L1[key]:
                for vec2 in L2[key]:
                    v=vec1[0]+vec2[0]
                    Av=vec1[1]+vec2[1]
                    if(
                        weight(v,1)==weight(v,q-1) and
                        weight(v,2)==weight(v,q-2) and
                        weight(v,3)==weight(v,q-3) and
                        inv_create_vec(v)==Nw_prevlevel
                    ):
                        assint=assign_int(g+(-1)**sign*(Av)[nrf_x:],q)
                        if assint in out:
                            out[assint]=insertion_bsearch(out[assint],(v, Av, assign_int(v,q)),2)
                        else:
                            out[assint]=[(v, Av, assign_int(v,q))]

    del(L1)
    del(L2)
    gc.collect()
    return out

def merge_lists_level_2(L1, L2, Nw_prevlevel, sign, g, q, eta):
    out={}
    count=0
    for key in L1:
        if key in L2:
            for vec1 in L1[key]:
                for vec2 in L2[key]:
                    v=vec1[0]+vec2[0]
                    Av=vec1[1]+vec2[1]
                    if(
                        weight(v,1)==weight(v,q-1) and
                        weight(v,2)==weight(v,q-2) and
                        weight(v,3)==weight(v,q-3) and
                        inv_create_vec(v)==Nw_prevlevel
                    ):
                        count+=1
                        odlyzko_hash=odlyzko(g+(-1)**sign*Av, eta, q)
                        for assint in odlyzko_hash:
                            if assint in out:
                                out[assint]=insertion_bsearch(out[assint],(v, Av, assign_int(v,q)),2)
                            else:
                                out[assint]=[(v, Av, assign_int(v,q))]
    del(L1)
    del(L2)
    gc.collect()
    return out

def merge_lists_level_1(L1, L2, Nw_prevlevel, t, q, eta):
    out_yes=[]
    out_no=[]
    for key in L1:
        if key in L2:
            for vec1 in L1[key]:
                for vec2 in L2[key]:
                    v=vec1[0]+vec2[0]
                    Av=vec1[1]+vec2[1]
                    if(
                        weight(v,1)==weight(v,q-1) and
                        weight(v,2)==weight(v,q-2) and
                        weight(v,3)==weight(v,q-3) and
                        inv_create_vec(v)==Nw_prevlevel and
                        eta_small(Av-t, eta, q)
                    ):
                        out_yes+=[v]
                    else:
                        out_no+=[v]
    del(L1)
    del(L2)
    gc.collect()
    return out_yes, out_no