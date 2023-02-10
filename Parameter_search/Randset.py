from random import randint

def drawbits(l):
    # draws l random bits
    out=""
    for i in range(l):
        out+=str(randint(0,1))
    return out

def str2bool(v):
    return v=="1"

def hamming(bstr):
    # yields the hamming weight of a binary vector
    out=0
    for i in range(len(bstr)):
        out+=int(bstr[i])
    return out

def create_randset(d, it1=0, it2=100, it3=100, it4=100, it5=0, it6=0, it7=0, it8=0):
    # a randset is used to dictate which parameters are supposed to be optimized,
    # where one 8-bit string denotes all parameters of a given d.
    
    # for example, the string '11111111' would denote that every parameter of a given level would be optimized,
    # while '11110000' dictates that only the Rep-2 parameters are to be optimized.
    
    # since there are l=8*(d-1) many parameters to optimize, we need strings of length l to dictate which
    # parameters should be optimized on all levels.
    
    # By default, we first optimize 2 parameters per level in 100 iterations (i.e. it2=100), then 3 parameters for 100 times
    # and then 4 parameters for 100 times. In other words, the number dictates the hamming weight of every 8-bit string.
    # We found that, after doing this for several rounds, it becomes more and more unlikely that we find better parameters.
    out=[]
    for ham in range(1,9):
        it=locals()['it'+str(ham)]
        for j in range(it):
            randstr=""
            for k in range(d):
                partstr=8*"0"
                while hamming(partstr)!=ham:
                    partstr=drawbits(8)
                randstr+=partstr
            out+=[randstr]
    return out