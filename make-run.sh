#!/bin/bash
# make-run.sh
# make sure core is always running.

echo 'a' > /home/hpdb/text.x
source "/home/hpdb/.bashrc"
echo $HPDB_BASE > /home/hpdb/text.x
if ps ax | grep -v grep | grep runcore > /dev/null
then
  exit
else         
  /home/hpdb/base/scripts/runcore &
fi