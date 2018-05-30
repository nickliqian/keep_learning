from __future__ import division
import matplotlib.pyplot as plt
from ising import *
import os
import numpy as np

Ns = [10, 20, 50, 100, 1000]  # System Size
T_Tcs = np.linspace(0.5, 1.7, 30)  # T/Tc
Tc = 2.268  # Onsager's Tc

for n in Ns:
    avgspins = []
    for i, T_Tc in enumerate(T_Tcs):
        T = T_Tc*Tc
        indices, spins = np.loadtxt('magnetization/size-{0}/temp-{1}/temp-{1}.out'.format(n,i), unpack =True)
        spins = spins[int(len(spins)/2):]
        avgspin = np.sum(np.abs(spins)) / n ** 2 / len(spins)
        avgspins.append(avgspin)
    plt.plot(T_Tcs, avgspins, 'o-', label = 'L = {0}'.format(n))

plt.xlabel('T/T$_{c}$', fontsize = 16)
plt.ylabel('<M$_{L}$>', fontsize = 16)
plt.legend()
plt.savefig('images/magnetization.png')
plt.show()