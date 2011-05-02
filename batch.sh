#!/bin/bash
#$ -q development
#$ -A TG-STA060015N
#$ -V
#$ -cwd
#$ -N mpi4py-demo
#$ -j y
#$ -o $JOB_NAME.o$JOB_ID
#$ -pe 12way 12
#$ -l h_rt=00:05:00
#$ -M 6075920299@vtext.com
#$ -m be

# Let it write tiny, tiny core files so we see something went wrong.
ulimit -c 1

set -x

python receiver.py&

python logtest.py

ibrun python sample.py --loghost `hostname`

pkill python
