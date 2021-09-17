import numpy as np

pf_trunc = np.loadtxt("./PF/E-f22-n10-p20000_abs.txt")
pf_feist = np.loadtxt("./Feist/E-f22-n10-p20000_abs.txt")
pf_coup = np.loadtxt("./pf-2/E-f22-n10-p20000_abs_just_coup.txt")

# print(f"Test {pf_trunc[:,0]}")

coup_con = pf_coup[:,0:20] - pf_trunc[:,0:20] 
coup_con[:,0] = pf_trunc[:,0]

dse_con = pf_feist[:,0:20] - pf_trunc[:,0:20]
dse_con[:,0] = pf_trunc[:,0]

np.savetxt("dws_coup_con.txt", coup_con)
np.savetxt("dws_dse_con.txt", dse_con)
np.savetxt("dws_added.txt", dse_con + coup_con)