#!/software/anaconda3/2020.07/bin/python
#SBATCH -A action -p action 
#SBATCH -o output1.log
#SBATCH --mem-per-cpu=4GB
#SBATCH -t 10:00:00
#SBATCH -n 12
#SBATCH -N 1
import numpy as np
from multiprocessing import Pool
import time , sys, os
sys.path.append(os.popen("pwd").read().replace("\n",""))
from polariton import Ĥ, param
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
sbatch = [i for i in open('par_coup_pf2.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
cpu   = int(sbatch[-2].split()[-1].replace("\n","")) #int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
nodes = int(sbatch[-1].split()[-1].replace("\n",""))
print (os.environ['SLURM_JOB_NODELIST'], os.environ['SLURM_JOB_CPUS_PER_NODE'])
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
#-------------------------------------
E = np.loadtxt("../Hm/E.txt")
N = len(E[0,1:])

R = E[:,0]
R_0 = 0.0
R_ind = np.argmin(np.absolute(R - R_0))
print (f"R index = {R_ind}")
E = E[:,1:]

µ = np.loadtxt("../Hm/µ.txt")[:,1:]

eta = np.linspace(0.0, 1.0, 128)
#-----------------------------------------
print (f"Total states available : {N}")
#-----------------------------------------
with Pool(len(eta)) as p:
    #------ Arguments for each CPU--------
    args = []
    for j in range(len(eta)):
        par = param() 
        par.ns = ns
        par.η_1 = eta[j]
        par.η_3 = eta[j] / np.sqrt(3)
        par.χ_1 = par.ωc * par.η_1
        par.χ_3 = par.ωc * par.η_3 * 3

        #----------------------
        H   = np.zeros((N, N))
        H[np.diag_indices(N)] = E[R_ind,:]
        par.H = H[:ns,:ns]
        par.µ = µ[R_ind,:].reshape((N,N))[:ns,:ns]
        param.nf = nf
        param.ns = ns
        Hij = Ĥ(par)
        args.append(Hij)

    #-------- parallelization --------------- 
    result  = p.map(np.linalg.eigh, args)
    #----------------------------------------
t2 = time.time() - t0 
print (f"Time taken: {t2} s")
print (f"Time for each point: {t2/len(eta)} s")
#------- Gather -----------------------------
E, _ = result[0]
E = np.zeros((len(E)+1, len(eta)))

for Ri in range(len(eta)):
    E[1:,Ri] = result[Ri][0] 
#---- Shift ZPE ----------
E0 = np.min(E[1,:]) # ZPE
E[1:,:] -= E0

for n in range(len(E[1,:])):
    E[1:,n] = E[1:,n] - E[1,n]
#-------------------------
E[0,:] = eta
#--------------------------------------------
np.savetxt(f"E-f{nf}-n{ns}-R{R_0}_Feist.txt", E.T)