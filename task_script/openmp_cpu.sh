#!/bin/bash               
#SBATCH -J openmp_cpu_job
#SBATCH -p skl
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
#SBATCH --time 00:30:00
#SBATCH --comment etc    # See Application SBATCH options name table's

export OMP_NUM_THREADS=10

module purge
module load intel/18.0.2

./test_omp.exe

exit 0

