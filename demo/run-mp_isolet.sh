#!/usr/bin/bash
#
# Author: James Henderson
# Updated: November 17, 2021
# 79: -------------------------------------------------------------------------

# slurm options: --------------------------------------------------------------
#SBATCH --job-name=mp_isolet-gb0
#SBATCH --mail-user=jbhender@umich.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=5GB 
#SBATCH --time=10:00
#SBATCH --account=cscar
#SBATCH --partition=standard
#SBATCH --output=/home/%u/logs/%x-%j-4.log

# application: ----------------------------------------------------------------
n_procs=4

# modules 
module load tensorflow

# the contents of this script
cat run-mp_isolet.sh

# run the script
date

cd /home/jbhender/github/Stats507_F21/demo/
python mp_isolet.py $n_procs

date
echo "Done."
