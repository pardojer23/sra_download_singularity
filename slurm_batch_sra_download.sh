#!/bin/bash
#SBATCH --job-name=sra
#SBATCH --mem=32Gb
#SBATCH --ntasks=16
#SBATCH --time=3:59:59
#SBATCH --output=sra_%A_%a.out

SAMPLE_LIST=($(<sample_file_list.txt))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
SRA_TOOLS="/mnt/research/VanBuren_Lab/01_code/04_containers/sra_tools.simg"
echo ${SAMPLE}
OUTPUT=$1
singularity run ${SRA_TOOLS} fasterq-dump ${SAMPLE} --outdir ${OUTPUT} --threads 12

