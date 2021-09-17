import numpy as np  
import math 
from numpy import linalg as LA
from numpy import kron as ꕕ
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

def momentum(re):
    N = float(len(re))
    mass = 1.0
    p = np.zeros((int(N),int(N)))
    Rmin = float(re[0])
    Rmax = float(re[-1])
    step = float((Rmax-Rmin)/N)
    K = np.pi/step

    for ri in range(int(N)):
        for rj in range(int(N)):
            if ri == rj:  
                p[ri,ri] = 0.5 * K
            else:    
                p[ri,rj] = 1j * (-1)**(rj-ri) / (step * ((rj-ri))) 
    return p


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
    return He #, nac(R, V,param)

def ĉ(nf):
    a = np.zeros((nf,nf))
    for m in range(1,nf):
        a[m,m-1] = np.sqrt(m)
    return a.T

def Ĥ(param):
    Hm = Hel(param)
    nf = 10
    
    p = momentum(param.re)

    #---------------------------------------------
    ωc = 0.4/27.2114
    η_1  = 0.15
    χ_1 = ωc * η_1
    #------------------------
    Iₚ_1 = np.identity(nf).astype("complex")
    Iₘ = np.identity(len(param.re)).astype("complex")
    #------ Photonic Part -----------------------
    Hₚ_1 = np.identity(nf).astype("complex")
    Hₚ_1[np.diag_indices(nf)] = np.arange(nf) * ωc
    â = ĉ(nf) 
    #------ Vector Potential --------------------
    A0_1 = χ_1/ωc
    Â_1 = A0_1 * (â.T + â)

    Hij = Hm
    # Hij   = ꕕ(Hm, Iₚ_1)     # Matter
    # Hij  += ꕕ(Iₘ, Hₚ_1)     # Photon 1
    # Hij  -= ꕕ(p, Â_1)    # Interaction 1
    # Hij  += ꕕ(Iₘ, Â_1 @ Â_1) * 0.5  # Diamagnetic term 1

    E, V = Diag(Hm)

    return E 

# def nac(R, V,param):
#     re = param.re 
#     dR = 0.00001
#     V1 = Ve(R+dR, re, param) 
#     V2 = Ve(R-dR, re, param) 
#     T = Te(re, param) 
#     E1, V1 = Diag(T + V1) 
#     E2, V2 = Diag(T + V2) 
#     dc = np.zeros((param.states,param.states)) 
#     for i in range(param.states):
#         for j in range(param.states):
#             if (i!=j):
#                 sign =  (V1[:,j] * V2[:,j])/np.abs((V1[:,j] * V2[:,j]))
#                 dV = (V1[:,j] - sign * V2[:,j]) / (2.0 * dR)
#                 dc[i,j] = np.sum(V[:,i] * dV) 
#             else :
#                 dc[i,i] = 0.0
#     return dc 
    


 
# def mu(R, V, param):
#     dm = np.zeros((param.states,param.states)) 
#     for i in range(param.states):
#         for j in range(param.states):
#             dm[i,j] = - np.sum(param.re  * V[:,i]  * V[:,j] ) + R * (i==j) 
#     return dm 
# """
# def pij(R, V, param):
#     pm = np.zeros((param.states,param.states)) 
#     for i in range(param.states):
#         for j in range(param.states):
#             dm[i,j] = - np.sum(param.re  * V[:,i]  * V[:,j] ) + R * (i==j) 
#     return dm 
# """
au = 0.529177249 # A to a.u.
# Parameters 2b
class param:
    mass = 1836.0
    R1 = -3.5/ au
    R2 = 3.5/ au
    Z1 = 1.0 
    Z2 = 1.0
    Rc = 1.75/ au
    Rn = 1.0/ au
    re = np.linspace(R1 - 40, R2 + 40, 10000)
    R  = 0


if __name__=="__main__":
    fob = open("pes.txt", "w+") 
    # dmfob = open("dm.txt", "w+") 
    # nacfob = open("nac.txt", "w+") 
    Ri = float(sys.argv[1])
    param.R = Ri
    # dm, Ei, ddr = Hel(param) 
    dm, Ei, ddr = Hel(param) 
    fob.write(str(Ri) + "\t" + "\t".join(Ei.astype("str")) + "\n")
    # dmfob.write(str(Ri) + "\t" + "\t".join(dm.flatten().astype("str")) + "\n")
    # nacfob.write(str(Ri) + "\t" + "\t".join(ddr.flatten().astype("str")) + "\n")
    fob.close()
    # dmfob.close()
    # nacfob.close()