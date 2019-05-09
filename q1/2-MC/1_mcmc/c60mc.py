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

def MCMC_Ising(beta, num, l_local, l_total):
    """
    Parameters:
        beta  The temperature $\beta=1/(kT)$
        num   The number of equilibrium configuration data
    Returns:
        res   The euqilibrium Ising spin configuration data
        Z     The partition function of the Ising spin model.
    """
    cut = 10000000   #The cut of iteration
    iterations = cut+num
    res = np.zeros((num, 60))
    
    x = np.random.randint(-1,1,60)
    E_total = totalE(x,l_total)

    Energy_chain = []
    #M_chain = []
    Z_chain = []
    labelvalueseri = np.random.randint(0, 60, iterations)

    for i in range(iterations):
        #print("i=", i)
        labelvalue = labelvalueseri[i]
        E_0 = localE(x, labelvalue, l_local)
        E_change = -2*E_0
        x[labelvalue] = -x[labelvalue]
        E_total = E_total+E_change

        if E_change >0:
            probability = np.exp(-beta*E_change)
            if np.random.rand()>probability:
                x[labelvalue] = -x[labelvalue]
                E_total = E_total - E_change
            
        if i>cut-1:
            res[i-cut] = x
            #M_chain.append((np.sum(x)*(np.sum(x)))/60.)  ##Calculate magnetization
            Energy_chain.append(E_total)    ##Calculate Energy
            #Z_chain.append(np.exp(-beta*E_total))    ##Calculate the exp E
    return res, np.mean(Energy_chain)

if __name__=="__main__":
    beta = 1.    #temperature
    num = 100000
    c60labelEdge = np.load('data/c60labelEdge.npy') #The edge pair labels of c60 lattice
    c60labelNode = np.load('data/c60labelNode.npy') #The nearist-node labels of c60 lattice
    #print('c60labelEdge:',c60labelEdge)
    #print('c60labelNode:',c60labelNode)
#    x = np.ones(60)
#    TE = totalE(x, c60labelEdge)
#    print('TE',TE)

    config_c60, E = MCMC_Ising(beta, num, c60labelNode, c60labelEdge)
    print('E=',E)
    
    datafile = 'data/mcdata.dat'
    with open(datafile, 'w') as f1:
        f1.write("SSH chanllenge 1\n")
        f1.write("beta=%.2f\n" % beta)
        f1.write("E=%.2f\n" % E)
    #for i in range(100):
    #    print('i=',i,'energypersite',ene[i]/60.)
