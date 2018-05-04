#!/bin/bash -l
#$ -l h_rt=0:12:00
#$ -N healthy_sim
#$ -wd /home/ucbpjru/Scratch
# Set up the job array.  In this instance we have requested 10000 tasks
# numbered 1 to 100.
#$ -t 1-10000

module load python3/recommended
cd $TMPDIR
export BASEDIR="$HOME/BayesCMD"

DATAFILE="$BASEDIR/PLOS_paper/data/simulated_smooth_combined_ABP.csv"
CONFIGFILE="$BASEDIR/examples/configuration_files/simulated_parameter_config.json"

start=`date +%s`
python3 $BASEDIR/batch_Bayes/batch.py 1000 $DATAFILE $CONFIGFILE --workdir $TMPDIR
echo "Duration: $(($(date +%s)-$start)) > $TMPDIR/$SGE_TASK_ID_timings.txt

tar zcvf $HOME/Scratch/batch_$JOB_NAME_$SGE_TASK_ID.tar.gz $TMPDIR
