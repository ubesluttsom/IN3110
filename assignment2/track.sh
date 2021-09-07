#!/bin/bash

cmd=$1
label=$2

if [ "$LOGFILE" == "" ]; then 
  LOGFILE=~/.local/share/timer_logfile
fi

prevcmd=$(tail -n 1 $LOGFILE 2>/dev/null | cut -d' ' -f 1 -)

if [ "$#" -eq "0" ]; then
  echo "usage: track start [label]"
  echo "       track stop"
  echo "       track status"
  exit 0
fi

if [ "$cmd" == "start" ]; then
  if [ "$prevcmd" == "START" ] || [ "$prevcmd" == "LABEL" ] ; then
    echo "Can't start new task concurrent to previous. (End it first.)"
    exit 0
  else
    echo "START $(date)" | tee -a $LOGFILE
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
    echo "END $(date)" | tee -a $LOGFILE
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
