from Searchspace_Representations import *
from Eps import leveleps
from math import isnan, isinf

#evl_T and evl_L both take an initial distribution as well as a parameter set and calculate each level's respective Time (or space) to create any search list of said level.

def evl(dist, d, eps, retT=True, retL=True):
    T=[0]
    L=[0]
    w=[dist]
    S=[searchspace(w[0])]
    R=[1]
    for j in range(1,d):
        leps=leveleps(eps,j)
        w+=[cw(w[j-1],leps)]
        T+=[0]
        S+=[searchspace(w[j])]
        R+=[representations(w[j-1],leps)]
        L+=[S[j]-R[j]]
        if j==d-1:
            R=R+[0]
            L=L+[S[j]/2]
            T=T+[S[j]/2]
            if isnan(R[j]) or isinf(R[j]):
                T[j]=-R[j]
            elif isnan(R[d]) or isinf(R[d]):
                T[j]=R[d]
            else:
                T[j]=2*L[d]-R[j]
        if j>1:
            if isnan(R[j]) or isinf(R[j]):
                T[j-1]=-R[j]
            elif isnan(R[j-1]) or isinf(R[j-1]):
                # there appears to be a weird error where R[j-1] can be either NaN or inf, I attribute it to rounding.
                # So far, this error has not occured in the neighborhood of optimal parameters, 
                # so we assume that it has no impact on the optimization itself.
                T[j-1]=-R[j-1]
            else:
                T[j-1]=2*L[j]-(R[j-1]-R[j])
        elif isnan(R[1]) or isinf(R[1]):
            T[0]=-R[1]
        else:
            T[0]=max(0,2*L[1]-1)
    for j in range(d):
        T[j]=max(T[j],L[j+1])
    T[d]=L[d]
    if retT and retL:
        return [T,L]
    elif retT:
        return T
    elif retL:
        return L
    return []

def evl_T(dist, d, eps):
    return evl(dist, d, eps, retT=True, retL=False)

def evl_L(dist, d, eps):
    return evl(dist, d, eps, retT=False, retL=True)