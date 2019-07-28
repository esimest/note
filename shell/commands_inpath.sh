#!/bin/bash

# How many commands: a simple script to count how many executable
#   commands are in your current PATH

. ansi_color.sh

IFS=":"
count=0 ;  nonex=0

for directory in $PATH ; do
  if [ -d "$directory" ] ; then
    for command in "$directory/*" ; do  # 效果和 "$directory/*"
      echo -e "$yellowf$command$reset"
      if [ -x "$command" ] ; then
        count="$(( $count + 1 ))"
      else
        nonex="$(( $nonex + 1 ))"
      fi
    done
  fi
done

echo "$count commands, and $nonex entries that weren't executable"
exit 0
