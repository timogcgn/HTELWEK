from random import sample

def insertion_bsearch(L,x,index):
    low=0
    high=len(L)-1
    while low<=high:
        mid=(low+high)//2

        if L[mid][index]<x[index]:
            low=mid+1
        elif L[mid][index]>x[index]:
            high=mid-1
        else:
            return L
    if high==-1:
        return [x]+L
    else:
        return L[:low]+[x]+L[low:]

def bsearch_component(L,x,index):
    return bsearch_component_iter(L,0,len(L)-1,x,index)

def bsearch_component_iter(L,low,high,x,index):
    if high<low:
        return []
    elif high==low:
        if L[low][index]==x:
            true_low=low
            true_high=low
            while true_low>=0 and L[true_low][index]==x:
                true_low-=1
            true_low+=1
            while true_high<len(L) and L[true_high][index]==x:
                true_high+=1
            true_high-=1
            return L[true_low:true_high+1]
        else:
            return []
    else:
        mid=int((high+low)/2)
        if L[mid][index]>x:
            return bsearch_component_iter(L,low,mid-1,x,index)
        elif L[mid][index]<x:
            return bsearch_component_iter(L,mid+1,high,x,index)
        else:
            true_low=mid
            true_high=mid
            while true_low>=0 and L[true_low][index]==x:
                true_low-=1
            true_low+=1
            while true_high<len(L) and L[true_high][index]==x:
                true_high+=1
            true_high-=1
            return L[true_low:true_high+1]
            
def assign_int(v,q):
    out=0
    for i in range(len(v)):
        out+=int(v[i])*q**i
    return out  
            
def inv_assign_int(x,q,N):
    out=[]
    y=x
    while y>0:
        w=y%q
        out=[w]+out
        y=(y-w)//q
    out=(N-len(out))*[0]+out
    return out  