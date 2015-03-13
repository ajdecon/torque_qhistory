#!/bin/bash
# Created 2013-05-03 by derekgottlieb
#
# Grind through torque accounting logs in a specified directory
# 1. Pitch any jobs that don't have all 3 (Q/S/E) events
# 2. Put all 3 events into single file based on E month

# Sample accounting entry:
# 04/01/2013 23:00:41;Q;8.mds1.asc.edu;queue=small-parallel

if [ -z $1 ]; then
 echo "Usage: $0 completed_prefix [accounting_dir]"
 exit
fi

if [ -z $2 ]; then
 if [ -z $PBS_SERVER_PRIV ]; then
  echo "Must define PBS_SERVER_PRIV env var or specify as arg"
  exit
 fi
 SRCACCTDIR="$PBS_SERVER_PRIV/accounting"
else
 SRCACCTDIR="$2"
fi

PREFIX="$1"
OUTDIR="/tmp/$USER/torque_accounting_$PREFIX"
ACCTDIR="$OUTDIR/tmp"

echo "Placing results in $OUTDIR..."

mkdir -p $OUTDIR
rm -rf $OUTDIR/*

mkdir -p $OUTDIR/tmp
cp $SRCACCTDIR/* $ACCTDIR/

alljobs=$(grep ";E;" ${ACCTDIR}/${PREFIX}* | cut -d';' -f3 | sort -n | uniq)

alljobs_count=$(echo -e "$alljobs" | wc -l)
echo "Found $alljobs_count completed jobs total in ${ACCTDIR}/${PREFIX}* files..."

processed_jobs=0
excluded_jobs=0

for job in $alljobs
do
 jobevents=$(grep --no-filename $job ${ACCTDIR}/*)
 found_q=$(echo -e "$jobevents" | grep ";Q;" | wc -l)
 found_s=$(echo -e "$jobevents" | grep ";S;" | wc -l)
 found_e=$(echo -e "$jobevents" | grep ";E;" | wc -l)
 #found_d=$(echo -e "$jobevents" | grep ";D;" | wc -l)

 #echo "$job: $found_q Q, $found_s S, $found_e E, $found_d D"

 if [ $found_q -eq 1 ] && [ $found_s -eq 1 ] && [ $found_e -eq 1 ]; then
  # Have queue, start, and end events, determine month and add all 3 to that
  # month's accounting log
  ENDDATE=$(echo -e "$jobevents" | grep ";E;" | awk '{print $1}' | awk 'BEGIN {FS="/"} {print $3 $1}')
  echo -e "$jobevents" >> $OUTDIR/$ENDDATE
  processed_jobs=$((processed_jobs+1))
  echo "$job processed... ($processed_jobs)"
 else
  excluded_jobs=$((excluded_jobs+1))
  echo "$job excluded... ($excluded_jobs)"
 fi
done

echo "$alljobs_count jobs total = $processed_jobs processed + $excluded_jobs excluded"

