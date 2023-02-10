from random import sample, shuffle
from numpy import array

from Odlyzko import odlyzko

def GFsample(q):
    return sample(range(0,q),1)[0]

def create_vec(Nw, q, shuffling=False):
    out=int(Nw[0])*[0]
    for i in range(1,len(Nw)):
        out+=int(Nw[i])*[i]
        out+=int(Nw[i])*[q-i]
    if shuffling:
        shuffle(out)
    return out

def inv_create_vec(vec):
    out=5*[0]
    for i in vec:
        if int(i)<5:
            out[i]+=1
    return out

def create_vec_d(Nw,N):
    Halfw=5*[0]
    for i in range(5):
        Halfw[i]=Nw[i]
    Halfw[0]-=int(N/2)
    return create_vec(Halfw,q)