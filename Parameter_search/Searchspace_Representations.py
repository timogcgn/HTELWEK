from scipy.stats import entropy
from Entropy_Functions import quentropy

def searchspace(w):
    # given an input list w, this function returns the entropy of a search space where, for entries from the scale [-eta,eta] (for eta=len(w)+1), an entry i appears relatively w[i] many times
    v=[w[0]]
    for i in range(1,len(w)):
        v=v+[w[i]]
        v=v+[w[i]]
    return entropy(v,base=2)

def representations(w,eps):
    # this function calculates, given a previous level search space list w and a parameter set, the amount of representations from an entry of upper search spaces with entries from lower levels that are distributed according to eps
    rep0=quentropy([eps[10],eps[10],eps[20],eps[20],eps[30],eps[30]],w[0])
    rep1=quentropy([eps[21],eps[21],eps[31],eps[31],(w[1]-2*eps[21]-2*eps[31])/2,(w[1]-2*eps[21]-2*eps[31])/2],w[1],incomplete=False)
    rep2=quentropy([eps[22],eps[22],eps[32],eps[32]],w[2])
    rep3=quentropy([eps[33],eps[33],(w[3]-2*eps[33])/2,(w[3]-2*eps[33])/2],w[3],incomplete=False)
    return (2*rep3+2*rep2+2*rep1+rep0)

# the cw functions calculate, according to the previous search space parameters pw and a parameter set eps, the search space for the current level
def cw1(pw, ce):
    return (pw[1]+2*pw[2]+pw[3]-2*ce[33]-2*ce[32]-2*ce[31]+2*ce[10]-4*ce[22])/2

def cw2(pw, ce):
    return (pw[3]+2*pw[4]+2*ce[20]+2*ce[21]+2*ce[22]+2*ce[31]-2*ce[33])/2

def cw3(pw, ce):
    return (2*ce[33]+2*ce[32]+2*ce[31]+2*ce[30])/2

def cw(pw, ce):
    c1=cw1(pw, ce)
    c2=cw2(pw, ce)
    c3=cw3(pw, ce)
    c0=1-2*(c1+c2+c3)
    return [c0,c1,c2,c3,0]