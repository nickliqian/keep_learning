from ising import *
import os
import numpy as np

Ns = [10, 20, 50, 100, 1000]  # System Size
T_Tcs = np.linspace(0.5, 1.7, 30)  # T/Tc
Tc = 2.268  # Onsager's Tc

for n in Ns:
    for i, T_Tc in enumerate(T_Tcs):
        T = T_Tc*Tc
        wd = 'magnetization/size-{0}/temp-{1}'.format(n, i)
        if not os.path.exists(wd): 
            os.makedirs(wd)
        if n !=1000:
            write_job_script(wd=wd, n=n, s= n * 1000000, T=T, i=i)
        else:
            write_job_script(wd=wd, n=n, s= n * 1000000, T=T, i=i, nprocs = 1, q ='long')
        run_job(wd)