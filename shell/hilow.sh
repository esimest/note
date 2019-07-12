#!/bin/bash

# hilow-- A simple num-guessing game

# import validint.sh ansi_color.sh
. validint.sh
. ansi_color.sh

biggest=100
guess=0
guesses=0

initializeANSI

# $$ : 当前进程的 pid

num=$(( $$ % biggest ))
echo "Guess a num betwwen 1 and $biggest"

while [ "$guess" != $num ]; do
  echo -n "Guess? " ; read guess
  validint $guess
  if [ ! $? -eq 0 ]; then
    echo -e "$redf Input is a valid ineger within your constraints.$reset"
  else
    if [ "$guess" -lt $num ]; then
      echo "... bigger!"
    elif [ "$guess" -gt $num ]; then
      echo "... smaller!"
    fi
    guesses=$(( $guesses + 1 ))
  fi
done

echo "Right!! Guessed $num in $guesses guesses"

exit 0
