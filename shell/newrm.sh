#!/bin/bash

# newrm-- A replacement for the existing rm command.
#   This script provides a rudimentary unremove capability by creating and
#   utilizing a new directory within the user's home directory. It can handle
#   directories of content as well as individual files. If the user specifies
#   the -f flag, files are removed and NOT archived

#   Big Important Warning: You'll want a cron job or something similar to keep
#   the trash directories tamed. Otherwise, nothing will ever actually
#   be deleted from the system, and you'll run out of disk space!

archivedir="$HOME/.deleted-files"
realrm="$(which rm | grep '/rm')"
copy="$(which cp | grep '/cp') -R"

if [ $# -eq 0 ] ; then
  exec $realrm
fi

# Parse all options looking for '-f'

flags=""

while getopts "dfiPRrvW" opt
do
  case $opt in
    f ) exec $realrm "$@"      ;;  # exec lets us exit this script directly.
    * ) flags="$flags -$opt"   ;;  # Other flags are for rm, not us. { $flags += "-$opt" }
  esac
done

shift $(( $OPTIND - 1))

# BEGIN MAIN SCRIPT
# =================

# import ansi_color.sh

. ansi_color.sh
initializeANSI

# Make sure that the $archivedir exists.

if [ ! -d $archivedir ] ; then
  if [ ! -w $HOME ] ; then
    echo -e "$redf $0 failedL can't create $archivedir in $HOME $reset" >&2
    exit 1
  fi
  mkdir -p $archivedir
  chmod 700 $archivedir    # A little bit of privacy, please
fi

for arg in $* ;
do
  newname="$archivedir/$(date "+%S.%M.%H.%d.%m").$(basename "$arg")"
  if [ -f "$arg" -o -d "$arg" ] ; then
    $copy "$arg" "$newname"
  fi
done

exec $realrm $flags "$@"
