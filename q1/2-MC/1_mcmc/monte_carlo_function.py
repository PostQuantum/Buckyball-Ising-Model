
#2D Ising Model Monte Carlo Simulation
from numpy import random
import numpy as np
from numba import jit


#some parameters
#iterations=800000
#dimension = 32

# Energy of the lattice
#k=dimension
#extract=np.arange(1,k+1)
#extract[k-1]=0

def total_energy(matrix):
    k = matrix.shape[0]
    extract=np.arange(1,k+1)
    extract[k-1]=0
    S=[matrix[m,n] for m in range(k) for n in range(k)]
    S1=[matrix[i,j] for i in range(k) for j in extract]
    S2=[matrix[i, j] for i in extract for j in range(k)]
    E=[S[n]*(S1[n]+S2[n]) for n in range(len(S))]
    return -np.sum(E)

#@jit('int32(int32[:,:],int32,int32)')
def local_energy(matrix, m, n):
    k = matrix.shape[0]
    list = [m + 1, n + 1, m - 1, n - 1]
    if list[0] > k - 1:
        list[0] = list[0] - k
    if list[1] > k - 1:
        list[1] = list[1] - k
    if list[2] < 0:
        list[2] = list[2] + k
    if list[3] < 0:
        list[3] = list[3] + k
    return -matrix[m, n] * (matrix[list[0], n] + matrix[m, list[1]] + matrix[list[2], n] + matrix[m, list[3]])


#Markov Chain
def Markov_chain(num,Temperature, dimension):

    Isingx = np.zeros((num, dimension, dimension))
    cut = 100000
    iteration = num+cut
    
    # create 2d spin lattice
    x_array = random.randint(0, 2, size=(dimension, dimension))
    x = x_array * 2 - 1
    #some useful matrix,parameters
    Energy_chain = []
    M_chain=[]
    MN_value=random.randint(0, dimension, size=(2, iteration))
    E_total=total_energy(x)

    for i in range(iteration):
        print("i=", i)
        m=MN_value[0,i]
        n=MN_value[1,i]
        E_0= local_energy(x,m,n)
        E_change=-2*E_0
        x[m, n] = -x[m, n]
        E_total = E_total+E_change

        if E_change >0:
            probability = np.exp(-E_change /Temperature)
            if random.rand()>probability:
                x[m, n] = -x[m, n]
                E_total = E_total - E_change
            
        M_chain.append((np.sum(x)*(np.sum(x)))/(dimension*dimension))
        Energy_chain.append(E_total)
        if i>cut-1:
            Isingx[i-cut] = x
    return Isingx


#####Old v
#Sampling and find the average energy
def E_M_C_X_value(T, dimension, iterations):
    cut=round(iterations/10)
    listEM=Markov_chain(iterations,T,dimension)
    E=np.mean(listEM[0][cut:])/(dimension*dimension)
    M=np.mean(listEM[1][cut:])/(dimension*dimension)
    C_cut=[np.var(listEM[0][i:i+cut])/((dimension*dimension)*T*T) for i in range(0,iterations,cut) ]
    X_cut=[np.var(listEM[1][i:i+cut])/((dimension*dimension)*T) for i in range(0,iterations,cut)]
    C=np.mean(C_cut[1:])
    X=np.mean(X_cut[1:])
    E_error=np.sqrt(np.var(listEM[0][cut:])/(len(listEM[0][cut:])))
    M_error=np.sqrt(np.var(listEM[1][cut:])/(len(listEM[1][cut:])))
    C_error=np.sqrt(np.var(C_cut[1:])/(len(C_cut[1:])))
    X_error=np.sqrt(np.var(X_cut[1:])/(len(X_cut[1:])))

    return [E,M,C,X,E_error,M_error,C_error,X_error]
