#!/software/anaconda3/2020.07/bin/python
#SBATCH -A action -p action 
#SBATCH -o output12.log
#SBATCH --mem-per-cpu=8GB
#SBATCH -t 2-00:00:00
#SBATCH -n 6
#SBATCH -N 1
import numpy as np
from multiprocessing import Pool
import time , sys, os
sys.path.append(os.popen("pwd").read().replace("\n",""))
from polariton import Ĥ, param, ĉ
from numpy import kron as ꕕ
#-------------------------------------
try: 
    nf = int(sys.argv[1]) #param.nf
    ns = int(sys.argv[2]) #param.ns
    print (f"Using matter-states: {ns}, and Fock-states: {nf}")
except:
    nf = param.nf
    ns = param.ns
    print (f"Default matter-states: {ns}, and Fock-states: {nf}")
η  = param.η_1
#-------------------------------------
t0 = time.time()
#----------------------------  SBATCH  ---------------------------------------------------
sbatch = [i for i in open('par_coup.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
cpu   = int(sbatch[-2].split()[-1].replace("\n","")) #int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
nodes = int(sbatch[-1].split()[-1].replace("\n",""))
print (os.environ['SLURM_JOB_NODELIST'], os.environ['SLURM_JOB_CPUS_PER_NODE'])
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
#-------------------------------------
points = 20000

E = np.loadtxt(f"../Hm/pes_{points}.txt")
N = len(E[:])

µ = np.loadtxt(f"../Hm/dm_{points}.txt")[:]

eta = 0.25
omega_0 = E[1] - E[0]
omega = np.linspace(omega_0 / 100.0, 4.0 * omega_0, 128)
#-----------------------------------------
print (f"Total states available : {N}")
#-----------------------------------------
with Pool(len(omega)) as p:
    #------ Arguments for each CPU--------
    args = []
    for j in range(len(omega)):
        par = param() 
        par.ωc = omega[j]
        par.ns = ns
        par.η_1 = eta
        par.η_3 = eta / np.sqrt(3)
        par.χ_1 = omega[j] * par.η_1
        par.χ_3 = omega[j] * par.η_3 * 3

        #----------------------
        H = np.zeros((N, N))
        H[np.diag_indices(N)] = E[:]
        par.H = H[:ns,:ns]
        par.µ = µ[:].reshape((N,N))[:ns,:ns]
        param.nf = nf
        param.ns = ns
        Hij = Ĥ(par)
        args.append(Hij)

    #-------- parallelization --------------- 
    result  = p.map(np.linalg.eigh, args)
    #----------------------------------------
t2 = time.time() - t0 
print (f"Time taken: {t2} s")
print (f"Time for each point: {t2/len(omega)} s")
#------- Gather -----------------------------
print ("Starting DSE and Coupling Calculations")
temp, _ = result[0]
e_length = len(temp)
E_new = np.zeros((e_length+1, len(omega)))
U = np.zeros((e_length, e_length))
dse_cont = np.zeros((e_length+1, len(omega)))
coup_cont = np.zeros((e_length+1, len(omega)))

par = param() 
par.ωc = E[1] - E[0]
par.ns = ns

Iₚ = np.identity(par.nf)
par.µ = µ[:].reshape((N,N))[:ns,:ns]
â = ĉ(nf)

t0 = time.time()
for omegai in range(len(omega)):
    par.ωc = omega[omegai]
    par.η_1 = eta
    par.η_3 = eta/ np.sqrt(3)
    par.χ_1 = omega[omegai] * par.η_1
    par.χ_3 = omega[omegai] * par.η_3 * 3

    E_new[1:,omegai] = result[omegai][0]
    U[:,:] = result[omegai][1]

    dse_cont[0,omegai] = omega[omegai]
    coup_cont[0,omegai] = omega[omegai]

    Dse3 = ꕕ(ꕕ(par.µ @ par.µ, Iₚ),Iₚ) * (par.χ_3**2/(3.0 * par.ωc))
    Coup3 = ꕕ(ꕕ(par.µ, Iₚ), (â.T + â)) * par.χ_3

    dse_tot = U.T @ Dse3 @ U 
    coup_tot = U.T @ Coup3 @ U

    # First Order
    for j in range(e_length):
        E_new[j+1, omegai] += dse_tot[j,j] + coup_tot[j,j]
        dse_cont[j+1,omegai] += dse_tot[j,j]
    
    E_omega = result[omegai][0]
    # Second Order
    for j in range (20):
        Ej = E_omega[j]
        for m in range (20):
            if  omegai != 0:
                if m != j:
                    Em = E_omega[m]
                    E_new[j+1, omegai] += (dse_tot[j,m] + coup_tot[j,m])*(dse_tot[m,j] + coup_tot[m,j]) / (Ej - Em)
                    # E_new[j+1, omegai] += (coup_tot[j,m])*(coup_tot[j,m]) / (Ej - Em)
                    dse_cont[j+1,omegai] += (dse_tot[j,m])*(dse_tot[m,j]) / (Ej - Em)
                    coup_cont[j+1, omegai] += (coup_tot[j,m])*(coup_tot[j,m]) / (Ej - Em)
    
        
t2 = time.time() - t0 
print (f"Time taken: {t2} s")
print (f"Time for each point: {t2/len(omega)} s")


#---- Shift ZPE ----------
E0 = (E_new[1,0]) # ZPE
E_new[1:,:] -= E0

# for n in range(len(E[1,:])):
#     E[1:,n] = E[1:,n] - E[1,n]
#-------------------------
E_new[0,:] = omega
#--------------------------------------------
np.savetxt(f"E-f{nf}-n{ns}-p{points}_abs_omega_wide.txt", E_new.T)
np.savetxt(f"DSE-f{nf}-n{ns}-p{points}_omega_wide.txt", dse_cont.T)
np.savetxt(f"Coup-f{nf}-n{ns}-p{points}_omega_wide.txt", coup_cont.T)
np.savetxt(f"Add-f{nf}-n{ns}-p{points}_omega_wide.txt", coup_cont.T + dse_cont.T)