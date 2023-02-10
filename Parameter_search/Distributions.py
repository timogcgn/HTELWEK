from Entropy_Functions import pbin

def etadist(eta):
    # centered binomial search space where each entry appears pbin(i) many times. Is now called centered_binom_search
    w=max(5,eta+1)*[0]
    c=max(5,eta+1)*[0]
    for i in range(0,eta+1):
        w[i]=pbin(eta,i)
    return w

def centered_binom_dist(eta):
    return etadist(eta)

def unidist(eta):
    # creates a uniformly distributed search space
    List=(eta+1)*[1/(2*eta+1)]
    while len(List)<5:
        List+=[0]
    return List

def terdist(weight):
    # ternary search space where w[1]=weight
    w=[1-2*weight,weight,0,0,0]
    return w