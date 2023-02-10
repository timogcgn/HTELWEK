from random import sample

def unidist(eta):
    List=(eta+1)*[1/(2*eta+1)]
    while len(List)<5:
        List+=[0]
    return List

def unisample(eta,q):
    return (sample(range(-eta,eta+1),1)[0])%q

def unituple(eta,q,N):
    out=[]
    for i in range(N):
        out+=[unisample(eta,q)]
    return out