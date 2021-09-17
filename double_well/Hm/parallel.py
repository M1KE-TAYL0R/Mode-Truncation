#!/software/anaconda3/2020.07/bin/python
#SBATCH -A action -p action 
#SBATCH -o output.log
#SBATCH --mem-per-cpu=12GB
#SBATCH -t 10:00:00
#SBATCH -n 1
#SBATCH -N 1
import numpy as np
from multiprocessing import Pool
import time , sys, os
sys.path.append(os.popen("pwd").read().replace("\n",""))
import SM 
t0 = time.time()
print ()
#----------------------------  SBATCH  ---------------------------------------------------
sbatch = [i for i in open('parallel.py',"r").readlines() if i[:10].find("#SBATCH") != -1 ]
cpu   = int(sbatch[-2].split()[-1].replace("\n","")) #int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
nodes = int(sbatch[-1].split()[-1].replace("\n",""))

print (os.environ['SLURM_JOB_NODELIST'], os.environ['SLURM_JOB_CPUS_PER_NODE'])
print (f"nodes : {nodes} | cpu : {cpu}")
procs = cpu * nodes
#----------------------------------
#----------------------------------
try:
    print (sys.argv[1])
    print (sys.argv[2])
    print (sys.argv[3])
    R = np.linspace(float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]))
except:
    print (f"Default Settings")
    R = np.linspace(-4,4,24*8)
with Pool(1) as p:
    #------ Arguments for each CPU--------
    args = []
    for j in range(1):
        par = SM.param() 
        args.append(par)
    #-------- parallelization --------------- 
    result  = p.map(SM.Hel, args)
    #----------------------------------------
t2 = time.time() - t0 
print (f"Time taken: {t2} s")
print (f"Time for each point: {t2/len(R)} s")
#------- Gather -----------------------------
µ0, E0, _ = result[0]
sh = len(µ0.flatten())
µ = np.zeros( (sh+1 , len(R)) )
E = np.zeros((len(E0)+1, len(R)) )
dij = np.zeros((len(E0)**2+1, len(R)) )
for Ri in range(len(R)):
    µ[1:,Ri] = result[Ri][0].flatten()
    E[1:,Ri] = result[Ri][1].flatten()
    dij[1:,Ri] = result[Ri][2].flatten()
    # save R
    µ[0,Ri], E[0,Ri], dij[0,Ri] = R[Ri], R[Ri], R[Ri]
    
#--------------------------------------------
np.savetxt("µ.txt", µ.T)
np.savetxt("E.txt", E.T)
np.savetxt("dij.txt", dij.T)