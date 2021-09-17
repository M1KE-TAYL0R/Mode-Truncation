import numpy as np 
import os
Rl = np.linspace(-4,4,40)
os.system("rm -rf R-*")
for iRl in range(len(Rl)-1):
    Rmn = Rl[iRl]
    point = 5
    Rmx = np.linspace(Rl[iRl],Rl[iRl+1],point+1)[-2]
    test = 'R-'+ str(iRl)
    os.mkdir(test)
    os.chdir(test)
    os.system("cp ../SM.py ./")
    os.system("cp ../parallel.py ./")
    print('sbatch parallel.py ' + str(Rmn) + ' ' + str(Rmx) + ' ' + str(point))
    os.system(f'sbatch parallel.py ' + str(Rmn) + ' ' + str(Rmx) + ' ' + str(point))
    os.chdir(f"../")
