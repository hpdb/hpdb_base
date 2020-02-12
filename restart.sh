#!/bin/bash
# restart.sh
# restart pipeline

kill $(ps aux | grep -e 'runcore' | grep -v 'grep' | awk '{print $2}') > /dev/null 2>&1
./make-run.sh