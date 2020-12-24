#!/bin/bash
#SBATCH -J hybrid_cpu_job
#SBATCH -p skl
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
#SBATCH --time 00:30:00
#SBATCH --comment etc     # See Application SBATCH options name table's 

export OMP_NUM_THREADS=5

module purge
module load intel/18.0.2 mpi/impi-18.0.2

srun ./test_omp.exe

