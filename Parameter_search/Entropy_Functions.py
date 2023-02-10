from scipy.stats import entropy
from scipy.special import comb

def pbin(eta,i):
    # centered binomial distribution probabilities
    return comb(2*eta,eta+i)/(2**(2*eta))

def quentropy(A,scale, incomplete=True):
    # scaled entropy. This function automatically completes the input set to 1; should this lead to errors due to rounding, use incomplete=False. Is designed to scale with the scaling factor of the binomial coefficient.
    if scale==0:
        return 0
    for i in range(len(A)):
        A[i]=A[i]/scale
    if incomplete:
        A=A+[1-sum(A)]
    return scale*entropy(A,base=2)