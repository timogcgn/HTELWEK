from Distributions import centered_binom_dist
from Evaluate import evl_T, evl_L
from math import ceil

# tableprint returns a latex-compilable table of List sizes and run times for a given distribution and a specific parameter set. If no specific distribution is entered, this function assumes the CBD
# Unless one wants to create latex compilable tables, this part of the code can be ignored in its entirety

def tableprint(name, eps, eta=3, d=4, dist=[], treatzero=" ", ifthrees=True, ifcolor=True, iftop=False, ifbottom=False):
    if dist==[]:
        dist=centered_binom_dist(eta)
    pdist=dist #leftover from old version
    P="0" #leftover from old version
    T=evl_T(pdist,d,eps)
    L=evl_L(pdist,d,eps)
    max_T= max(T)
    max_L= max(L)
    for i in range(len(T)):
        if T[i]==max_T:
            T[i]="\mathbf{" + "{:0.3f}".format((ceil(T[i]*1000))/1000) + "}N"
            if T[i][:9]=="\mathbf{0":
                T[i]="\mathbf{" + T[i][9:]
        else:
            T[i]="{:0.3f}".format((ceil(T[i]*1000))/1000) + "N"
            if T[i][0]=="0":
                T[i]=T[i][1:]
        if L[i]==max_L:
            L[i]="\mathbf{" + "{:0.3f}".format((ceil(L[i]*1000))/1000) + "}N"
            if L[i][:9]=="\mathbf{0":
                L[i]="\mathbf{" + L[i][9:]
        else:
            L[i]="{:0.3f}".format((ceil(L[i]*1000))/1000) + "N"
            if L[i][0]=="0":
                L[i]=L[i][1:]
    initeps={}
    for key in eps:
        if eps[key]>0:
            initeps[key]=("{:0.3f}".format((round(eps[key]*1000))/1000))[1:]
        else:
            initeps[key]=treatzero
    line_segment="\\hhline{~|" + ifstring(ifcolor, ">{\\arrayrulecolor{Gray}}->{\\arrayrulecolor{black}}", nots="~") + "|*{" + ifstring(ifthrees, "8", nots="4") + "}{-}|~|" + ifstring(ifcolor, ">{\\arrayrulecolor{Gray}}->{\\arrayrulecolor{black}}", nots="~") + "}"
    if iftop:
        printtop(ifthrees=ifthrees, ifcolor=ifcolor)
    print("        \\multirow{"+ str(d+1) + "}*{$" + name + "$}")
    print("        &0&\\multicolumn{" + ifstring(ifthrees, "8", nots="4") + "}{c|}{-}&$" + T[0] + "$&$" + L[0] + "$" + "\\\\" + line_segment)
    for j in range(1,d-1):
        print("        &" + str(j) + "&$" + initeps[10,j] + "$&$" + initeps[20,j] + "$&$" + initeps[21,j] + "$&$" + initeps[22,j] + ifstring(ifthrees,"$&$" + initeps[30,j] + "$&$" + initeps[31,j] + "$&$" + initeps[32,j] + "$&$" + initeps[33,j]) + "$&$" + T[j] + "$&$" + L[j] + "$\\\\")
    print("        &" + str(d-1) + "&$" + initeps[10,d-1] + "$&$" + initeps[20,d-1] + "$&$" + initeps[21,d-1] + "$&$" + initeps[22,d-1] + ifstring(ifthrees,"$&$" + initeps[30,d-1] + "$&$" + initeps[31,d-1] + "$&$" + initeps[32,d-1] + "$&$" + initeps[33,d-1]) + "$&$" + T[d-1] + "$&$" + L[d-1] + "$\\\\" + line_segment)
    print("        &" + str(d) + "&\\multicolumn{" + ifstring(ifthrees, "8", nots="4") + "}{c|}{-}&$" + T[d] + "$&$" + L[d] + "$\\\\\\hline")
    if ifbottom:
        printbottom()
        
def printtop(ifthrees=True, ifcolor=True):
    print("% IMPORTANT: put \\usepackage{tabularx}, \\usepackage{multirow}, \\usepackage{hhline}, \\usepackage{xcolor, colortbl}, \\definecolor{Gray}{gray}{0.9} in your preamble")
    print("    \\begin{tabular}{c|" + ifstring(ifcolor, ">{\\columncolor{Gray}}") + "c|c" + ifstring(ifcolor, ">{\\columncolor{Gray}}c",nots="|c") + ifstring(ifcolor, "c",nots="|c") + ifstring(ifcolor, ">{\\columncolor{Gray}}c",nots="|c") + ifstring(ifthrees, ifstring(ifcolor, "c",nots="|c") + ifstring(ifcolor, ">{\\columncolor{Gray}}c",nots="|c") + ifstring(ifcolor, "c",nots="|c") + ifstring(ifcolor, ">{\\columncolor{Gray}}c",nots="|c")) + "|c|" + ifstring(ifcolor, ">{\\columncolor{Gray}}") + "c" + "}")
    print("        $\\mathcal D$&$j$&$\\epsilon_{10}^{(j)}$&$\\epsilon_{20}^{(j)}$&$\\epsilon_{21}^{(j)}$&$\\epsilon_{22}^{(j)}" + ifstring(ifthrees,"$&$\\epsilon_{30}^{(j)}$&$\\epsilon_{31}^{(j)}$&$\\epsilon_{32}^{(j)}$&$\\epsilon_{33}^{(j)}") + "$&$\\mathcal T^{(j)}$&$\\mathcal L^{(j)}$" + "\\\\\\hline")

def printbottom():
    print("    \\end{tabular}")
    
def ifstring(b,s,nots=""):
    if b:
        return s
    else:
        return nots