#!/bin/bash
# make-run.sh
# make sure core is always running.

source '/home/hpdb/.hpdb'
if ps ax | grep -v grep | grep runcore > /dev/null
then
  exit
else         
  /home/hpdb/base/scripts/runcore &
fi