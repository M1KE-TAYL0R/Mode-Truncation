#!/software/anaconda3/2020.07/bin/python
#SBATCH -A action -p action 
#SBATCH -o output1.log
#SBATCH --mem-per-cpu=5GB
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
sbatch = [i for i in open('parallel.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
cpu   = int(sbatch[-2].split()[-1].replace("\n","")) #int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
nodes = int(sbatch[-1].split()[-1].replace("\n",""))
print (os.environ['SLURM_JOB_NODELIST'], os.environ['SLURM_JOB_CPUS_PER_NODE'])
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
#-------------------------------------
E = np.loadtxt("../Hm/E.txt")
N = len(E[0,1:])
R = E[:,0]
E = E[:,1:]
µ = np.loadtxt("../Hm/µ.txt")[:,1:]
#-------------------------------------
ns = min(ns,N)
with Pool(len(R)) as p:
    #------ Arguments for each CPU--------
    args = []
    for j in range(len(R)):
        par = param() 
        par.ns = ns
        #----------------------
        H   = np.zeros((N, N))
        H[np.diag_indices(N)] = E[j,:]
        par.H = H[:ns,:ns]
        par.µ = µ[j,:].reshape((N,N))[:ns,:ns]
        param.nf = nf
        param.ns = ns
        Hij = Ĥ(par)
        args.append(Hij)

    #-------- parallelization --------------- 
    result  = p.map(np.linalg.eigh, args)
    #----------------------------------------
t2 = time.time() - t0 
print (f"Time taken: {t2} s")
print (f"Time for each point: {t2/len(R)} s")
#------- Gather -----------------------------
E, _ = result[0]
E = np.zeros((len(E)+1, len(R)))

for Ri in range(len(R)):
    E[1:,Ri] = result[Ri][0] 
#---- Shift ZPE ----------
E0 = np.min(E[1,:]) # ZPE
E[1:,:] -= E0
#-------------------------
E[0,:] = R
#--------------------------------------------
np.savetxt(f"E-f{nf}-n{ns}-η{η}.txt", E.T)