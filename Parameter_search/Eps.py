from numpy import sign
from math import floor

# In general, we use dictionaries for parameter sets. In this program, they are referred to as "eps".

def nulleps(d):
    # creates a parameter set of level depth with entry 0 for all epsilon-entries
    out={}
    for i in (10,20,21,22,30,31,32,33):
        for j in range(1,d+1):
            out[i,j]=0
    return out

def leveleps(eps, level):
    #returns all epsilon entries of a specific level
    out={}
    for i in [10,20,21,22,30,31,32,33]:
        out[i]=eps[i,level]
    return out

def copyeps(eps, epsscale=1, changeeps={},changescale=1):
    #copies a parameter set. Can also be used to combine two sets, i.e. when using the gd search for a new library
    out={}
    for key in eps:
        if changeeps=={}:
            out[key]=eps[key]*epsscale
        else:
            out[key]=eps[key]*epsscale+changeeps[key]*changescale
    return out

def formateps(eps,d, levelfirst=False, reverselevelfirst=False):
    # takes any input eps and turns it into a eps of the epsilon-format.
    out={}
    if levelfirst:
        for j in range(1,d):
            for i in [10,20,21,22,30,31,32,33]:
                if (i,j) in eps:
                    out[i,j]=eps[i,j]
                else:
                    out[i,j]=0
    elif reverselevelfirst:
        for k in range(1,d):
            j=d-k
            for i in [10,20,21,22,30,31,32,33]:
                if (i,j) in eps:
                    out[i,j]=eps[i,j]
                else:
                    out[i,j]=0
    else:
        for i in [10,20,21,22,30,31,32,33]:
            for j in range(1,d):
                if (i,j) in eps:
                    out[i,j]=eps[i,j]
                else:
                    out[i,j]=0
    return out

def roundeps(eps,digits=3):
    # takes an input eps and rounds its entries
    out={}
    for key in eps:
        out[key]=round((10**(digits+1)*eps[key]))/(10**(digits+1))
    return out

def ideps(eps):
    # this function requires no explanation
    return eps

def counteps(eps):
    out=0
    for key in eps:
        if eps[key]!=0:
            out+=1
    return out

def lightningeps(eps, scale, gamma=0.001):
    out={}
    for key in eps:
        if eps[key]==0:
            out[key]=[0]
        else:
            out[key]=[]
            sig=sign(eps[key])
            for l in range(1,scale+1):
                out[key]+=[sig*l*gamma]
    return out

def normaleps(eps, gamma):
    out={}
    for key in eps:
        out[key]=sign(eps[key])*gamma
    return out

def fullbintruthdict(bstr):
    out={}
    d=floor((len(bstr)-1)/8)
    for j in range(d+1):
        out[10,j+1]=bstr[j*8+0]=='1'
        out[20,j+1]=bstr[j*8+1]=='1'
        out[21,j+1]=bstr[j*8+2]=='1'
        out[22,j+1]=bstr[j*8+3]=='1'
        out[30,j+1]=bstr[j*8+4]=='1'
        out[31,j+1]=bstr[j*8+5]=='1'
        out[32,j+1]=bstr[j*8+6]=='1'
        out[33,j+1]=bstr[j*8+7]=='1'
    return out