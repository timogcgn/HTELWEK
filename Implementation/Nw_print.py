from Multinomial import multinomial

def Nw_print(Nw, rf, q, eta):
    d=len(Nw)-1
    N=2*sum(Nw[0])-Nw[0][0]
    for negj in range(0,d-1):
        j=d-negj
        print("---------- " + str(j) + " ----------")
        print("Search Space is:")
        print([Nw[j]])
        print("")
        print("Expected full list size:")
        fullsize=multinomial([int(Nw[j][0]),int(Nw[j][1]),int(Nw[j][1]),int(Nw[j][2]),int(Nw[j][2])])/q**rf[j]
        print(float(fullsize))
        print("")

    print("---------- " + str(1) + " ----------")
    print("Search Space is:")
    print([Nw[1]])
    print("")
    print("Expected full list size:")
    fullsize=multinomial([int(Nw[1][0]),int(Nw[1][1]),int(Nw[1][1]),int(Nw[1][2]),int(Nw[1][2])])/q**rf[1]*(1+N*(2*eta+1)/q)
    print(float(fullsize))