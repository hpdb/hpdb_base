#!/bin/bash
# make-run.sh
# make sure core is always running.

source "/home/hpdb/.bashrc"
echo $HPDB_BASE
if ps ax | grep -v grep | grep runcore > /dev/null
then
  exit
else         
  /home/hpdb/base/scripts/runcore &
fi