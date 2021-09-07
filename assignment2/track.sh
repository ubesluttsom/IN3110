#!/bin/bash

cmd=$1
label=$2

# Define LOGFILE when not an environment variable
if [ "$LOGFILE" == "" ]; then 
  LOGFILE=~/.local/share/timer_logfile
fi

# Extract last command/action from logfile (and silence "file not found")
prevcmd=$(tail -n 1 $LOGFILE 2>/dev/null | cut -d' ' -f 1 -)

if [ "$#" -eq "0" ]; then
  echo "usage: track start [label]"
  echo "       track stop"
  echo "       track status"
  echo "       track log"
  exit 0
fi

if [ "$cmd" == "start" ]; then
  if [ "$prevcmd" == "START" ] || [ "$prevcmd" == "LABEL" ] ; then
    echo "Can't start new task concurrent to previous. ('track stop' first.)"
    exit 0
  else
    echo "START $(date +'%a %b %e %H:%M:%S %Z %Y')" | tee -a $LOGFILE
    if [ "$label" == "" ]; then
      label='<null>'
    fi
    echo "LABEL $label" | tee -a $LOGFILE
    exit 1
  fi
fi

if [ "$cmd" == "stop" ]; then
  if [ "$prevcmd" != "START" ] && [ "$prevcmd" != "LABEL" ] ; then
    echo "No current task."
    exit 0
  else
    echo "END $(date +'%a %b %e %H:%M:%S %Z %Y')" | tee -a $LOGFILE
    exit 1
  fi
fi

if [ "$cmd" == "status" ]; then
  if [ "$prevcmd" == "START" ] || [ "$prevcmd" == "LABEL" ] ; then
    echo "Currently tracking:"
    echo "$(tail -n 2 $LOGFILE)"
    exit 1
  else
    echo "No current task."
    exit 1
  fi
fi

if [ "$cmd" == "log" ]; then
  grep "LABEL" $LOGFILE | cut -d' ' -f 2 | while read LABEL;
  do
    # Extract START and END times for each label:
    # `grep`: find right lines (notice before/after-context)
    # `sed`:  delete line with "LABEL" keyword
    # `cut`:  extract time (to spesific format for `date`)
    START=$(grep --max-count=1 --before-context=1 "$LABEL" $LOGFILE | \
            sed -e '/LABEL/d' | \
            cut -d' ' -f 4,3,7,5,6)
    END=$(grep --max-count=1 --after-context=1 "$LABEL" $LOGFILE | \
          sed -e '/LABEL/d' | \
          cut -d' ' -f 4,3,7,5,6)
    # Convert START and END times to UTC seconds
    START=$(date --utc --date "$START" +"%s")
    END=$(date --utc --date "$END" +"%s")
    # Print LABEL; use `date` to calculate elapsed seconds & convert format
    echo "${LABEL}: $(date --utc -d "0 $END sec - $START sec" +'%H:%M:%S')"
  done
fi
