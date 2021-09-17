import numpy as np

pf_trunc = np.loadtxt("./PF_Fiest_Trunc/E-f60-n18-η0.15.txt")
pf_feist = np.loadtxt("./PF_Fiest_Trunc/E-f60-n18-η0.15_Feist.txt")
pf_coup = np.loadtxt("./PF_two/E-f18-n10-η0.15_just_coup.txt")

# print(f"Test {pf_trunc[:,0]}")

coup_con = pf_coup[:,0:20] - pf_trunc[:,0:20] 
coup_con[:,0] = pf_trunc[:,0]

dse_con = pf_feist[:,0:20] - pf_trunc[:,0:20]
dse_con[:,0] = pf_trunc[:,0]

np.savetxt("SM_coup_con.txt", coup_con)
np.savetxt("SM_dse_con.txt", dse_con)
np.savetxt("SM_added.txt", dse_con + coup_con)