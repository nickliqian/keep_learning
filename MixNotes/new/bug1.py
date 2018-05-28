import numpy as np


def init_lattice(n):
    '''Create a nxn lattice with random spin configuration'''

    lattice = np.random.choice([1, -1], size=(n, n))
    return lattice


def deltaE(S0, Sn, J, H):
    '''Energy difference for a spin flip'''

    return 2 * S0 * (H + J * Sn)


def ising(n=200,
          nsteps=500000,
          H=0,
          J=1,
          T=1,
          count_spins=False,
          countij=[1, 1],
          correlation=False,
          corr_ij=[0, 0],
          corr_r=1):
    '''Ising Model Simulator. If count_spins = True, only flipping behavior of 1 site is studied.'''

    lattice = init_lattice(n)
    energy = 0
    energies = []
    spins = []
    spin = np.sum(lattice)
    icount, jcount = countij
    counted_spins = [lattice[icount, jcount]]
    counted_intervals = []
    icorr, jcorr = corr_ij
    Sis = []
    SiSjs = []

    for step in range(nsteps):

        i = np.random.randint(n)
        j = np.random.randint(n)

        # Periodic Boundary Condition
        Sn = lattice[(i - 1) % n, j] + lattice[(i + 1) % n, j] + \
             lattice[i, (j - 1) % n] + lattice[i, (j + 1) % n]

        dE = deltaE(lattice[i, j], Sn, J, H)

        if dE < 0 or np.random.random() < np.exp(-dE / T):
            lattice[i, j] = -lattice[i, j]
            energy += dE
            energies.append(energy)
            # Note that the spin is collected at every step
            spin += 2 * lattice[i, j]

        if count_spins:
            ispin = lattice[icount, jcount]
            if ispin != counted_spins[-1]:
                counted_spins.append(ispin)
                counted_interval = step - sum(counted_intervals)

                counted_intervals.append(counted_interval)
        if correlation:
            Sn_corr = lattice[(icorr - corr_r) % n, jcorr] + lattice[(icorr + corr_r) % n, jcorr] + \
                      lattice[icorr, (jcorr - corr_r) % n] + lattice[icorr, (jcorr + corr_r) % n]
            Si = lattice[icorr, jcorr]
            SiSj = Si * Sn_corr / 4.0
            Sis.append(Si)
            SiSjs.append(SiSj)

        spins.append(spin)

    if correlation:
        return Sis, SiSjs

    if count_spins:
        return counted_spins, counted_intervals

    return lattice, energies, spins


def ising1000(n=1000, nsteps=10000000000, H=0, J=1, T=1):
    '''Ising Model Simulator. Special case for very large lattices.
    To reduce some memory usage:
    spin is added to the array every 1000 steps.
    Energies are not returned.
    Still pretty inefficient!
    '''

    lattice = init_lattice(n)
    energy = 0

    spins = []
    spin = np.sum(lattice)
    for istep, step in enumerate(range(nsteps)):

        i = np.random.randint(n)
        j = np.random.randint(n)

        # Periodic Boundary Condition
        Sn = lattice[(i - 1) % n, j] + lattice[(i + 1) % n, j] + \
             lattice[i, (j - 1) % n] + lattice[i, (j + 1) % n]

        dE = deltaE(lattice[i, j], Sn, J, H)

        if dE < 0 or np.random.random() < np.exp(-dE / T):
            lattice[i, j] = -lattice[i, j]
            energy += dE
            spin += 2 * lattice[i, j]
        if istep % 1000 == 0:
            spins.append(spin)
    return lattice, spins


def write_job_script(wd='./', n=10, s=1000, i=1, T=1., nprocs=1, pe='smp', name='batch', q='long'):
    '''
    This is a function that writes a script to submit MC jobs
    '''
    py_file = '/afs/crc.nd.edu/user/p/pmehta1/ising-monte-carlo/spins.py'
    script = '''#!/bin/bash
#$ -N {0}
#$ -pe {1} {2}
#$ -q {3}
#$ -cwd
'''.format(name, pe, nprocs, q)

    if nprocs > 1:
        cmd = 'mpirun -np $NSLOTS python'
        script += '{6} {5} -n {0} -s {1} -i {2} -t {3} -w {4}'.format(n, s, i, T, wd, py_file, cmd)

    else:
        script += 'python {5} -n {0} -s {1} -i {2} -t {3} -w {4}'.format(n, s, i, T, wd, py_file)

    with open('{0}/qscript'.format(wd), 'w') as f:
        f.write(script)


def run_job(wd):
    '''
    Submit job to the queue
    '''
    import os
    from subprocess import Popen, PIPE
    cwd = os.getcwd()
    print("***", cwd)
    print("&&&", wd)
    os.chdir(wd)
    p = Popen(['qsub', 'qscript'], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

    if out == '' or err != '':
        raise Exception('something went wrong in qsub:\n\n{0}'.format(err))
    jobid = out.split()[2]
    f = open('jobid', 'w')

    f.write(jobid)
    f.close()
    os.chdir(cwd)
    return out.strip()


"""
n=200,
nsteps=500000,
T=1,
"""

# 以下看不懂了......
import sys, getopt, os

opts, args = getopt.getopt(sys.argv[1:], 'n:s:i:t:w')


# python bug1.py -n2 -s3 -i6 -t8 -w
# python bug1.py -n数字 -s数字 -i数字 -t数字 -w 文件
# 传入指定的参数和文件
for key, val in opts:

    if key == '-n':
        n = int(val)
    elif key == '-s':
        nsteps = int(val)
    elif key == '-t':
        T = float(val)
    elif key == '-i':
        index = int(val)
    elif key == '-w':
        wd = str(val)

# 生成指定的参数
if n < 500:
    lattice, energies, spins = ising(n=n, nsteps=nsteps, T=T)
    # print("lattice {}".format(lattice))
    # print("energies {}".format(energies))
    print("spins {}".format(spins))
else:
    lattice, spins = ising1000(n=n, nsteps=nsteps, T=T)
    print("2: ", lattice, spins)
    print("---")

# 'temp-{1}.out'.format(wd, index) temp-{index}.out -i
with open(os.path.join(wd, 'temp-{1}.out'.format(wd, index)), 'w') as f:
    for i, spin in enumerate(spins):
        if i % 1000 == 0:
            f.write("{0}\t{1}\n".format(i, spin))

Ns = [10, 20, 50, 100, 1000]  # System Size
T_Tcs = np.linspace(0.5, 1.7, 30)  # T/Tc
Tc = 2.268  # Onsager's Tc

for n in Ns:
    for i, T_Tc in enumerate(T_Tcs):
        T = T_Tc * Tc
        wd = 'magnetization/size-{0}/temp-{1}'.format(n, i)
        if not os.path.exists(wd):
            os.makedirs(wd)
        if n != 1000:
            write_job_script(wd=wd, n=n, s=n * 1000000, T=T, i=i)
        else:
            write_job_script(wd=wd, n=n, s=n * 1000000, T=T, i=i, nprocs=1, q='long')
        run_job(wd)

import matplotlib.pyplot as plt

Ns = [10, 20, 50, 100, 1000]  # System Size
T_Tcs = np.linspace(0.5, 1.7, 30)  # T/Tc
Tc = 2.268  # Onsager's Tc

for n in Ns:
    avgspins = []
    for i, T_Tc in enumerate(T_Tcs):
        T = T_Tc * Tc
        indices, spins = np.loadtxt('magnetization/size-{0}/temp-{1}/temp-{1}.out'.format(n, i), unpack=True)
        spins = spins[int(len(spins) / 2):]
        avgspin = np.sum(np.abs(spins)) / n ** 2 / len(spins)
        avgspins.append(avgspin)
    plt.plot(T_Tcs, avgspins, 'o-', label='L = {0}'.format(n))

plt.xlabel('T/T$_{c}$', fontsize=16)
plt.ylabel('<M$_{L}$>', fontsize=16)
plt.legend()
plt.savefig('./magnetization.png')
plt.show()
