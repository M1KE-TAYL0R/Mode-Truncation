#!/software/anaconda3/2020.07/bin/python
#SBATCH -A action -p action 
#SBATCH -o output.log
#SBATCH --mem-per-cpu=12GB
#SBATCH -t 1:00:00
#SBATCH -n 1
#SBATCH -N 1

import numpy as np  
import math 
from numpy import linalg as LA
import sys
#----------------------------------------
# Matrix Diagonalization

def Diag(H):
    E,V = LA.eigh(H) # E corresponds to the eigenvalues and V corresponds to the eigenvectors
    return E,V
#----------------------------------------

# https://aip.scitation.org/doi/10.1063/1.468795 
def Coul(R, Zi, Zj, Rc):
    return Zi * Zj * (math.erf(abs(R)/Rc)/abs(R))  

def Vn(R, param):
    # R - R1 
    Vn1 = 1.0/abs(R-param.R1) #Coul(R-param.R1, 1.0, param.Z1, param.Rc)
    # R - R2 
    Vn2 = 1.0/abs(R-param.R2) #Coul(R-param.R2, 1.0, param.Z2, param.Rc)
    return Vn1 + Vn2 

def VeN(r, R, param):
    # re - R 
    Vn = Coul(r - R, -1.0, param.Z1, param.Rc)
    # re - R1 
    Vn1 = Coul(r - param.R1, -1.0, param.Z1, param.Rn)
    # re - R2 
    Vn2 = Coul(r - param.R2, -1.0, param.Z2, param.Rn)
    return Vn + Vn1 + Vn2 

# Kinetic energy for electron 
def Te(re,param):
 N = float(len(re))
 mass = 1.0
 Tij = np.zeros((int(N),int(N)))
 Rmin = float(re[0])
 Rmax = float(re[-1])
 step = float((Rmax-Rmin)/N)
 K = np.pi/step

 for ri in range(int(N)):
  for rj in range(int(N)):
    if ri == rj:  
     Tij[ri,ri] = (0.5/mass)*K**2.0/3.0*(1+(2.0/N**2)) 
    else:    
     Tij[ri,rj] = (0.5/mass)*(2*K**2.0/(N**2.0))*((-1)**(rj-ri)/(np.sin(np.pi*(rj-ri)/N)**2)) 
 return Tij
#---------------------------------

# 
def Ve(R, re, param):
    Vij =  np.zeros((len(re),len(re))) 
    for ri in range(len(re)):
        Vij[ri,ri] = VeN(re[ri], R, param) + Vn( R, param) 
    return Vij

def Hel(param):
    R = param.R
    re = param.re 
    V = Ve(R, re, param) 
    T = Te(re, param) 
    He = T + V 
    E, V = Diag(He)
    return V

def nac(R, V,param):
    re = param.re 
    dR = 0.00001
    V1 = Ve(R+dR, re, param) 
    V2 = Ve(R-dR, re, param) 
    T = Te(re, param) 
    E1, V1 = Diag(T + V1) 
    E2, V2 = Diag(T + V2) 
    dc = np.zeros((param.states,param.states)) 
    for i in range(param.states):
        for j in range(param.states):
            if (i!=j):
                sign =  (V1[:,j] * V2[:,j])/np.abs((V1[:,j] * V2[:,j]))
                dV = (V1[:,j] - sign * V2[:,j]) / (2.0 * dR)
                dc[i,j] = np.sum(V[:,i] * dV) 
            else :
                dc[i,i] = 0.0
    return dc 
    


 
def mu(R, V, param):
    dm = np.zeros((param.states,param.states)) 
    for i in range(param.states):
        for j in range(param.states):
            dm[i,j] = - np.sum(param.re  * V[:,i]  * V[:,j] ) + R * (i==j) 
    return dm 
"""
def pij(R, V, param):
    pm = np.zeros((param.states,param.states)) 
    for i in range(param.states):
        for j in range(param.states):
            dm[i,j] = - np.sum(param.re  * V[:,i]  * V[:,j] ) + R * (i==j) 
    return dm 
"""
au = 0.529177249 # A to a.u.
# Parameters 2b
class param:
    states = 20
    mass = 1836.0
    R1 = -3.5/ au
    R2 = 3.5/ au
    Z1 = 1.0 
    Z2 = 1.0
    Rc = 1.75/ au
    Rn = 1.0/ au
    re = np.linspace(R1 - 40, R2 + 40, 20000)
    R  = 0


if __name__=="__main__":
    param.R = 1.95
    V = Hel(param) 
    psi = np.zeros((len(V[:,0]),2))
    psi[:,0] = param.re  
    psi[:,1] = V[:,0] 
    psi = np.delete(psi, list(range(0, psi.shape[0], 2)), axis=0)
    psi = np.delete(psi, list(range(0, psi.shape[0], 2)), axis=0)
    np.savetxt("wf-%s.txt"%(param.R ),psi)