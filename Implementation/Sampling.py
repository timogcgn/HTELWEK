from random import sample, shuffle
from numpy import array

from Odlyzko import odlyzko

def GFsample(q):
    return sample(range(0,q),1)[0]

def create_vec(Nw_j, q, shuffling=False):
    out=int(Nw_j[0])*[0]
    for i in range(1,len(Nw_j)):
        out+=int(Nw_j[i])*[i]
        out+=int(Nw_j[i])*[q-i]
    if shuffling:
        shuffle(out)
    return out

def inv_create_vec(vec):
    out=5*[0]
    for i in vec:
        if int(i)<5:
            out[i]+=1
    return out

def create_vec_d(Nw_j, q):
    N=2*sum(Nw_j)-Nw_j[0]
    Halfw=5*[0]
    for i in range(5):
        Halfw[i]=Nw_j[i]
    Halfw[0]-=int(N/2)
    return create_vec(Halfw,q)