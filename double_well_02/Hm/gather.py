import os
import numpy as np
ls = [i for i in os.listdir() if i.find("R-") !=-1] 
ls0 = np.argsort([float(i.replace("R-","")) for i in ls])
ls = np.array(ls)
ls = ls[ls0[:-1]]
print (ls)
files = ['E.txt', 'µ.txt', 'dij.txt']

for idir in ls:
    for ifiles in files:
        with open(ifiles, "ab") as f:
            print (idir)
            try: 
                np.savetxt(f, np.loadtxt(f"{idir}/{ifiles}"))
            except:
                print (f"failed to load {idir}/{ifiles}")
    
    