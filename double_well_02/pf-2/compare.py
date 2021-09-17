import numpy as np

dse = np.loadtxt("DSE-f22-n10-p20000.txt")
dse = dse[:,0:20]

coup = np.loadtxt("Coup-f22-n10-p20000.txt")
coup = coup[:,0:20]

pf_trunc = np.loadtxt("../PF/E-f22-n10-p20000_abs.txt")
pf = np.loadtxt("E-f22-n10-p20000_abs.txt")

diff = pf[:,0:20] - pf_trunc[:,0:20] 
diff[:,0] = pf_trunc[:,0]

add = coup + 2.0 * dse
add[:,0] = pf_trunc[:,0]

np.savetxt("Add-f22-n10-p20000.txt", add)
np.savetxt("Diff-f22-n10-p20000.txt", diff)