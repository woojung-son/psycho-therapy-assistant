#!/bin/bash
#SBATCH -J woojung
#SBATCH -p ivy_v100_2 
#SBATCH -N 2
#SBATCH -n 4
#SBATCH -o %x.o%j
#SBATCH -e %x.e%j
#SBATCH --time 01:30:00
#SBATCH --gres=gpu:2
#SBATCH --comment tensorflow     # See Application SBATCH options name table's



srun python /scratch/kedu14/woojung/albert/mycode/albert_practice.py

