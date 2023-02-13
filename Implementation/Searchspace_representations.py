from Multinomial import multinomial
from Eps import *

def representations(Nw_next,eps):
    # this function calculates, given a next level search space list w and a parameter set, the non-asymptotic amount of representations
    N=2*sum(Nw_next)-Nw_next[0]
    rep0=multinomial([eps[10]*N,eps[10]*N,eps[20]*N,eps[20]*N,eps[30]*N,eps[30]*N,Nw_next[0]-(2*(eps[10]+eps[20]+eps[30]))*N])
    rep1=multinomial([eps[21]*N,eps[21]*N,eps[31]*N,eps[31]*N,Nw_next[1]//2-(2*eps[21]-2*eps[31])//2*N,Nw_next[1]//2-(2*eps[21]-2*eps[31])//2*N])
    rep2=multinomial([eps[22]*N,eps[22]*N,eps[32]*N,eps[32]*N,Nw_next[2]-(2*(eps[22]+eps[32]))*N])
    rep3=multinomial([eps[33]*N,eps[33]*N,Nw_next[3]//2-(2*eps[33])//2*N,Nw_next[3]//2-(2*eps[33])//2*N])
    return (rep0*(rep1*rep2*rep3)**2)

def searchspace(Nw_j):
    # given a distribution of entries in a vector, this function calculates the size of the search space
    out=[Nw_j[0]]
    for i in range(1,len(Nw_j)):
        out+=[Nw_j[i]]
        out+=[Nw_j[i]]
    return multinomial(out)

def level_descriptions(Nw, eps):
    for j in range(0,len(Nw)):
        print("---------- " + str(j) + " ----------")
        print("Nw[0]  = " + str(int(Nw[j][0])))
        print("Nw[1]  = " + str(int(Nw[j][1])))
        print("Nw[2]  = " + str(int(Nw[j][2])))
        print("Nw[3]  = " + str(int(Nw[j][3])))
        print("S[j]   = " + str(multinomial([int(Nw[j][0]),int(Nw[j][1]),int(Nw[j][1]),int(Nw[j][2]),int(Nw[j][2]),int(Nw[j][3]),int(Nw[j][3])])))
        if j==0:
            print("R[j]   = " + str(1))
        elif j==len(Nw)-1:
            print("R[j]   = " + str(representations(Nw[j-1],leveleps(nulleps(2), 1))))
        else:
            print("R[j]   = " + str(representations(Nw[j-1],leveleps(eps, j))))
        print("")