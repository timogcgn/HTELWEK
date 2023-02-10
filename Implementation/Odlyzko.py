from math import floor
from itertools import product

from Sort_search import assign_int

def odlyzkoset(eta ,q):
    return [(i)%q for i in range(-eta,eta+1)]+[(floor(q/2)+i)%q for i in range(-eta,eta+1)]

def odlyzko(v, eta, q, give_c=False):
    odset=odlyzkoset(eta,q)
    threshold=floor(q/2)
    odlyzko_cartesian=[]
    for i in range(len(v)):
        if v[i] in odset:
            odlyzko_cartesian+=[[0,1]]
        elif int(v[i])<threshold:
            odlyzko_cartesian+=[[0]]
        else:
            odlyzko_cartesian+=[[1]]
    cartesian=product(*odlyzko_cartesian)
    if give_c:
        return cartesian
    out=[]
    for item in cartesian:
        out+=[assign_int(item,2)]
    return out

def eta_small(v, eta, q):
    smallset=[(i)%q for i in range(-eta,eta+1)]
    for vi in v:
        if not(vi in smallset):
            return False
    return True