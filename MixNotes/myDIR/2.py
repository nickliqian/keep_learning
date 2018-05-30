import matplotlib.pyplot as plt
from ising import *
import numpy as np

temperatures = [0.5, 2.27, 5.0]

for T in temperatures:

    lattice, energies, spins = ising(n=20, nsteps = 500000, T=T)
    spins = np.array(spins) / 20. ** 2
    plt.plot(range(len(spins)), spins, label = 'T = {0}'.format(T))
plt.legend(loc = 'best')
plt.xlabel('nSteps')
plt.ylabel('Average Spin')
plt.ylim(-1.2, 1.2)
plt.savefig('images/average-spin.png')
plt.show()