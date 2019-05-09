#!/usr/bin/python
"""
c60mc gives yout the equilibrium configuration of the anti-ferromagnetic Ising model on the c60 lattice using the Monte Carlo simulation method.
"""
import numpy as np

def totalE(x, l):
    """
    Parmeters:
        x    The spin configuration on the Buckyball lattice.
        l    The Buckyball lattice edge labels.
    Returns:
        E    The total energy of the given spin configuration on the Buckyball lattice.
    """
    E = 0
    for i in range(90):
        E+=x[int(l[i,0])]*x[int(l[i,1])]
    return E

def localE(x, label, l):
    """
    Parmeters:
        x      The spin configuration on the Buckyball lattice.
        label  The one chosen site of the Buckyball lattice.
        l      The Buckyball lattice nearest node labels of one chosen site.
    Returns:
        E      The local energy on one site of the Buckyball lattice.
    """
    E = x[label]*x[int(l[label,0])]+x[label]*x[int(l[label,1])]+x[label]*x[int(l[label,2])]
    return E

def WangLandau(beta, l_local, l_total):
    """
    Parameters:
        beta  The temperature $\beta=1/(kT)$
    Returns:
    """
    cut = 10000000   #The cut of iteration
    f = 2.71828     ##The maltiplication factor
    
    g = np.ones(181)    ##[-90,90] energy range; EOS
    H = np.zeros(181)    ##[-90,90] energy range; Histogram
    
    x = np.random.randint(-1,1,60)
    E_total = totalE(x,l_total)
    while f>1.00000001:

        Energy_chain = []
        
        labelvalueseri = np.random.randint(0, 60, cut)

        for i in range(cut):
            print("i=", i)
            labelvalue = labelvalueseri[i]
            E_0 = localE(x, labelvalue, l_local)
            E_change = -2*E_0
            x[labelvalue] = -x[labelvalue]
            E1=E_total
            E_total = E_total+E_change
            E2=E_total

            #if E_change >0:
            #    probability = np.exp(-beta*E_change)
            #    if np.random.rand()>probability:
            #        x[labelvalue] = -x[labelvalue]
            #        E_total = E_total - E_change
            if g[E1+90]<g[E2+90]:
                proba = g[E1+90]/g[E2+90]
                if np.random.rand()>proba:
                    x[labelvalue] = -x[labelvalue]
                    E_total = E_total - E_change

            Energy_chain.append(E_total)    ## Energy Chain
            Elabel = E_total+90   ##Keep int
            g[Elabel] = g[Elabel]*f
            H[Elabel] +=1
            ##Decide if you do the next
         #   Hmeancut = 0.8*np.mean(H)              ###Debugging
         #   if i>10000:
         #       counter = 1
         #       for j in range(181):                   ###
         #           if H[j]!=0:
         #               if H[j]<Hmeancut:          ###Debugging
         #                   counter = 0
         #       if counter==1:
         #           break
        ##Do the next level random walk
        f = np.sqrt(f)
        print('f',f)
######################
    return g

if __name__=="__main__":
    beta = 1.    #temperature
    num = 100000
    c60labelEdge = np.load('data/c60labelEdge.npy') #The edge pair labels of c60 lattice
    c60labelNode = np.load('data/c60labelNode.npy') #The nearist-node labels of c60 lattice

    g = WangLandau(beta, c60labelNode, c60labelEdge)
    print('g=',g)
    
    datafile = 'data/mcdata.dat'
    with open(datafile, 'w') as f1:
        f1.write("SSH chanllenge 1\n")
        f1.write("beta=%.2f\n" % beta)
