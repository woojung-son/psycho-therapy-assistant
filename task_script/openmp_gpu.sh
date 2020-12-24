#!/bin/bash               
#SBATCH -J openmp_gpu_job
#SBATCH -p ivy_v100_2 
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
#SBATCH --time 00:30:00
#SBATCH --gres=gpu:2
#SBATCH --comment etc    # See Application SBATCH options name table's

export OMP_NUM_THREADS=10

module purge
module load intel/18.0.2 cuda/10.0

./test_omp.exe

exit 0

