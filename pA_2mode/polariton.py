import math
import time
import numpy as np
import scipy as sp
import sys
from numpy import linalg as LA
from numpy import kron as ꕕ
from numpy import array as A
#global xi
#xi = float(sys.argv[1])

def Eig(H):
    E,V = LA.eigh(H) # E corresponds to the eigenvalues and V corresponds to the eigenvectors
    return E,V
#-------------------------------------
#-------------------------------------
def ĉ(nf):
    a = np.zeros((nf,nf))
    for m in range(1,nf):
        a[m,m-1] = np.sqrt(m)
    return a.T

class param:
    H = A([[0,0],[0,1]])
    µ = A([[0,1],[1,0]])
    ns = 20
    nf = 20
    η_1  = 0.15
    η_3  = 0.15 / np.sqrt(3)
    ωc = 0.4/27.2114
    χ_1 = ωc * η_1
    χ_3 = ωc * η_3 * 3

#----------------------------------------
# Data of the diabatic states

def Ĥ(param):
    Hm = param.H.astype("complex")
    µ = param.µ
    ns = param.ns
    nf = param.nf
    #--------Delete Permanent Dipole -------------
    µ[np.diag_indices(param.ns)] = 0
    p = np.zeros(µ.shape,dtype='complex')
    for i in range(ns):
        for j in range(i+1,ns):
            p[i,j] = 1j * µ[i,j] * (Hm[i,i] - Hm[j,j])
            p[j,i] = - p[i,j]

    #---------------------------------------------
    ωc = param.ωc 
    χ_1 = param.χ_1
    χ_3 = param.χ_3
    #------------------------
    Iₚ_1 = np.identity(nf).astype("complex")
    Iₚ_3 = np.identity(nf).astype("complex")
    Iₘ = np.identity(ns).astype("complex")
    #------ Photonic Part -----------------------
    Hₚ_1 = np.identity(nf).astype("complex")
    Hₚ_1[np.diag_indices(nf)] = np.arange(nf) * ωc
    Hₚ_3 = np.identity(nf).astype("complex")
    Hₚ_3[np.diag_indices(nf)] = np.arange(nf) * ωc * 3.0
    â = ĉ(nf) 
    #------ Vector Potential --------------------
    A0_1 = χ_1/ωc
    A0_3 = χ_3/ωc/3.0
    Â_1 = A0_1 * (â.T + â)
    Â_3 = A0_3 * (â.T + â)
    #--------------------------------------------
    #       matter ⊗ photon 
    #--------------------------------------------
    # Hij   = ꕕ(ꕕ(Hm, Iₚ_1),Iₚ_3)     # Matter
    # Hij  += ꕕ(ꕕ(Iₘ, Hₚ_1),Iₚ_3)     # Photon 1
    # Hij  += ꕕ(ꕕ(Iₘ, Iₚ_1),Hₚ_3)     # Photon 3
    # Hij  -= ꕕ(ꕕ(p, Â_1),Iₚ_3)      # Interaction 1
    # Hij  -= ꕕ(ꕕ(p, Iₚ_1), Â_3)     # Interaction 3
    # Hij  += ꕕ(ꕕ(Iₘ, Â_1 @ Â_1) * 0.5,Iₚ_3)   # Diamagnetic term 1
    # Hij  += ꕕ(ꕕ(Iₘ, Iₚ_1) ,Â_3 @ Â_3) * 0.5  # Diamagnetic term 3

    Hij   = ꕕ(Hm, Iₚ_1)     # Matter
    Hij  += ꕕ(Iₘ, Hₚ_1)     # Photon 1
    Hij  -= ꕕ(p, Â_1)    # Interaction 1
    Hij  += ꕕ(Iₘ, Â_1 @ Â_1) * 0.5  # Diamagnetic term 1
    return Hij 
#--------------------------------------------------------

#----------------------------------------

if __name__ == "__main__":
 print (Ĥ(param))






