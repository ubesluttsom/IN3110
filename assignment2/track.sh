#!/bin/bash -x

cmd=$1
label=$2
LOGFILE=timer_logfile
prevcmd=$(tail -n 1 $LOGFILE | cut -d' ' -f 1 -)

if [ ! "$#" -eq 1 ]; then
  echo "USAGE: track start [label]"
  echo "       track stop"
  echo "       track status"
  exit 0
fi

if [ "${cmd}" == "start" ]; then
  if [ "$prevcmd" == "START" ]; then
    echo "Can't start new task concurrent to previous. (End it first.)"
    exit 0
  else
    echo "START $(date)" >> $LOGFILE
    exit 1
  fi
fi

if [ "${cmd}" == "stop" ]; then
  if [ "$prevcmd" != "START" ]; then
    echo "No current task."
    exit 0
  else
    echo "END $(date)" >> $LOGFILE
    exit 1
  fi
fi

if [ "${cmd}" == "status" ]; then
  if [ "$prevcmd" == "START" ]; then
    echo "Currently tracking: $(tail -n 1 $LOGFILE)"
    exit 1
  elif [ "$prevcmd" != "START" ]; then
    echo "No current task."
    exit 1
  fi
fi
