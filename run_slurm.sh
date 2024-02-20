#!/bin/bash
#
#SBATCH --job-name=ssowod
#SBATCH --qos=gpu-8
#SBATCH -n1
#SBATCH -N1
#SBATCH -p gpu
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:4
#SBATCH --output=logs/slurm-%j.out
#SBATCH --cpus-per-task=64

GPUS_PER_NODE=4 ./tools/run_dist_slurm.sh berz ssowformer 4 configs/OWOD_split_50.sh