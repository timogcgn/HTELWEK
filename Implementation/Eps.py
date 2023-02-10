def leveleps(eps, level):
    #returns all epsilon entries of a specific level
    out={}
    for i in [10,20,21,22,30,31,32,33]:
        out[i]=eps[i,level]
    return out

def nulleps(d):
    # creates a parameter set of level depth with entry 0 for all epsilon-entries
    out={}
    for i in (10,20,21,22,30,31,32,33):
        for j in range(1,d+1):
            out[i,j]=0
    return out