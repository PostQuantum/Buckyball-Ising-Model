#!/usr/bin/python
"""
c60tn gives you the partition funtion of the anti-ferromegnetic Ising model on the C60 lattice.
"""
import numpy as np
from scipy.linalg import sqrtm


def getBuckyball(B):
    """
    Parameters:
        B     Boltzmann matrix defined according to the Ising model
    Returns:
        res   The tensor on the Buckyball lattice
    """
    Bhalf = sqrtm(B)
    Site = np.zeros((2,2,2))
    for i in range(2):
        Site[i,i,i] = 1
    res = np.tensordot(Bhalf, Site, (1,0))
    res = np.tensordot(res, Bhalf, (1,1))
    res = np.tensordot(res, Bhalf, (1,1))
    return res

def getIcosahedron(T):
    """
    parameters:
        T     The tensor on the Buckyball lattice
    Returns:
        res   The tensor on the icosahedron lattice
    """
    T2 = np.tensordot(T, T, (2, 1))
    T3 = np.tensordot(T2, T, (3, 1))
    T5 = np.tensordot(T2, T3, ((3,1),(1,4)))
    res = T5
    tnorm = np.linalg.norm(np.reshape(res,(2*2*2*2*2)))
    lnz = np.log(tnorm)
    
    #T2check = np.tensordot(T, T, (1, 1))
    #nu = np.sum(abs(T2-T2check))
    #print('nu', nu)

    return lnz, res/tnorm

def getTetrahedron(lnz, T):
    """
    parameters:
        T     The tensor on the icosahedron lattice
    Returns:
        res   The tensor on the tetrahedron lattice
    """
    T2 = np.tensordot(T, T, (2, 3))
    T3 = np.tensordot(T2, T, ((2,6), (2,3)))
    res = np.reshape(T3, (8, 8, 8))
    tnorm = np.linalg.norm(np.reshape(res,(8*8*8)))
    lnz = lnz + np.log(tnorm)

    return lnz, res/tnorm

def getZ(lnz, T):
    """
    parameters:
        T     The tensor on the tetrahedron lattice
    Returns:
        res   The partition function
    """
    T2 = np.tensordot(T, T, (1,1))
    res = np.tensordot(T2, T2, ((0,1,2,3),(0,1,2,3)))
    res = np.log(res)+lnz

    return res

if __name__=="__main__":

    ##Anti-ferromagnetic Ising model on the Buckyball lattice
    beta = 1   #temperature
    B = np.array([[np.exp(-beta),np.exp(beta)],[np.exp(beta),np.exp(-beta)]])  #Boltzmann mattix
    #Bhalf = sqrtm(B)
    #[s,v,d] = np.linalg.svd(B)
    #print('sqrt',np.sqrt(v))
    #print('svd',s)
    #print('svd',v)
    #print('svd',d)
    Tbucky = getBuckyball(B).real
    print('bucky', Tbucky)
    #quit()
    lnz, Tico = getIcosahedron(Tbucky)
    print('ico=', Tico)
    lnz, Ttetra = getTetrahedron(lnz, Tico)
    print('tetra=', Ttetra)
    lnZ = getZ(lnz, Ttetra)
    print('The minus free energy of the system is', lnZ)
    #quit()
    lnZperSite = lnZ/60.
    print('The minus single site free energy is', lnZperSite)
