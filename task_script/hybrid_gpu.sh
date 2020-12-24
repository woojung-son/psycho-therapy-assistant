#!/bin/bash
#SBATCH -J hybrid_gpu_job
#SBATCH -p ivy_v100_2
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
#SBATCH --time 00:30:00
#SBATCH --gres=gpu:2
#SBATCH --comment etc     # See Application SBATCH options name table's 

export OMP_NUM_THREADS=5

module purge
module load intel/18.0.2 cuda/10.0 cudampi/mvapich2-2.3

srun ./test_omp.exe

