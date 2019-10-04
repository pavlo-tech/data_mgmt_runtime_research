import os
import sys
import random

nTrials = int(sys.argv[1])
seed = int (sys.argv[2])
random.seed(seed)
start = 0
if len(sys.argv) > 3:
    start = int(sys.argv[3])

step = 25
for i in range(start, nTrials, step):
    #os.system("mkdir test_" + str(i))
    ''' 
    outfile = open("fault" + str(i) + ".pbs", "w")
    outfile.write("#!/bin/bash\n"
                "#PBS -l nodes=1:ppn=16:xe\n"
                "#PBS -l walltime=0:60:00\n"
                "#PBS -q normal\n"
                "#PBS -j oe\n"
                "#PBS -A jr5\n"
                "#PBS -N SPMV_SDCPROP\n")

    for s in xrange(step):
        os.system("mkdir test_" + str(seed))
        outfile.write("cd $PBS_O_WORKDIR/test_" +str(seed)+"\n"
                    "aprun -n 1 /u/sciteam/jccalho2/research/sdcprop/tests/SpMV/SpMV.out /u/sciteam/jccalho2/research/sdcprop/tests/SpMV/aniso --stateFile /u/sciteam/jccalho2/research/FlipIt/.foo --numberFaulty 1 --faulty 0 " +  str(seed) + " &> /u/sciteam/jccalho2/research/sdcprop/tests/SpMV/test_" + str(seed) + "/test_" +str(seed) + ".txt\n")
        seed += 1
    outfile.close()
    '''
    print "Launching job", i
    os.system("qsub fault" + str(i) + ".pbs")
    #print "mpirun -np 1 ./SpMV.out ./aniso --stateFile /home/aperson/research/FlipIt/.spmv --numberFaulty 1 --faulty 0 " +  str(seed) + " > ./test_" + str(i) + "/test_" +str(i) + ".txt"
    #os.system("aprun -n 1 /u/sciteam/jccalho2/research/sdcprop/tests/SpMV/SpMV.out /u/sciteam/jccalho2/research/sdcprop/tests/SpMV/aniso --stateFile /u/sciteam/jccalho2/research/FlipIt/.foo --numberFaulty 1 --faulty 0 " +  str(seed) + " > ./test_" + str(i) + "/test_" +str(i) + ".txt")
    #os.system("mv log.*.txt ./test_" + str(i) + "/")

