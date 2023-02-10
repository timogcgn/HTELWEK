from random import sample
from scipy.special import comb

def pbin(eta,i):
    # centered binomial distribution probabilities
    return comb(2*eta,eta+i)/(2**(2*eta))

def centered_binom_dist(eta):
    w=max(5,eta+1)*[0]
    c=max(5,eta+1)*[0]
    for i in range(0,eta+1):
        w[i]=pbin(eta,i)
    return w

def cbdsample(eta,q):
    out=0
    for iterations in range(eta):
        out=out+sample([0,1],1)[0]-sample([0,1],1)[0]
    return out%q

def cbdtuple(eta,N,q):
    out=[]
    for i in range(N):
        out+=[cbdsample(eta,q)]
    return out