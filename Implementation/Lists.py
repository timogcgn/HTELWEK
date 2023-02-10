from Multinomial import multinomial
from statistics import median

def scale_list(L,scale):
    out=[]
    for i in range(len(L)):
        out+=[int(L[i]*scale)]
    return out

def weight(v,i):
    out=0
    for x in v:
        if x==i:
            out+=1
    return out

def diclen(dic):
    out=0
    for key in dic:
        out+=len(dic[key])
    return out

def avglen(a):
    if len(a)>0:
        return sum(a) / len(a)
    else:
        return 0
    
def eval_lists(avg_L, Nw, eta, q, rf):
    N=2*sum(Nw[0])-Nw[0][0]
    print("---------- " + str(0) + " ----------")
    print("min    = " + str(min(avg_L[0])))
    print("avg    = " + str(avglen(avg_L[0])))
    print("median = " + str(median(avg_L[0])))
    print("max    = " + str(max(avg_L[0])))
    print("E[L]   = " + str(1))

    for j in range(1,len(avg_L)):
        print("---------- " + str(j) + " ----------")
        print("min    = " + str(min(avg_L[j])))
        print("avg    = " + str(avglen(avg_L[j])))
        print("median = " + str(median(avg_L[j])))
        print("max    = " + str(max(avg_L[j])))
        if j==1:
            od_overhead=2**(N*(2*eta+1)/q)
        else:
            od_overhead=1
        fullsize=multinomial([int(Nw[j][0]),int(Nw[j][1]),int(Nw[j][1]),int(Nw[j][2]),int(Nw[j][2])])/q**rf[j]*od_overhead
        print("E[L]   = " + str(fullsize))
        print("")