#!/bin/bash

# unrm -- Searches the deleted files archive for the specified file or
#    directory. If there is more than one macthing result, it shows a list
#    of results ordered by timestamp and lets the user specify which one
#    to restore.

# import ansi_color.sh
. ansi_color.sh
initializeANSI

archivedir="$HOME/.deleted-files"
realrm="$(which rm | grep '/rm')"
move="$(which mv | grep '/mv')"

dest=$(pwd)

if [ ! -d $archivedir ] ; then
  echo -e "$redf $0: No deleted files directory: nothing to unrm $reset" >&2
  exit 1
fi
cd $archivedir

# If given no arguments, just show a listing of the deleted files.
if [ $# -eq 0 ] ; then
  echo -e "$yellowf Contents of your deleted files archive (sorted by date)"
  ls -FC | sed -e 's/\([[:digit:]][[:digit:]]\.\)\{5\}//g' -e 's/^/  /'
  echo -e "$reset"
  exit 0
fi

# Otherwise, we must have a user-specified pattern to work with.
#   Let's see if the pattern matches more than noe file or directory
#   in the archives.

matches="$(ls -d *"$1" 2> /dev/null |wc -l)"

if [ $matches -eq 0 ] ; then
  echo "$redf No match for '$1' in the deleted file archivedir. $reset" >&2
  exit 1
fi

if [ $matches -gt 1 ] ; then
  echo -e "$greenf More than one file or directory match in the archive:"
  index=1
  for name in $(ls -d *"$1") ; do
    datetime="$(echo $name | cut -c1-14 | \
      awk -F. '{ print $5"/"$4" at "$3":"$2":"$1}')"
    filename="$(echo $name | cut -c16-)"
    if [ -d $name ] ; then
      filecount="$(ls $name | wc -l |sed 's/[^[:digit:]]//g')"
      echo " $index)  $filename (contents = $filecount items," \
            " deleted = $datetime)"
    else
      size="$(ls -sdk1 $name | awk '{print $1}')"
      echo " $index)  $filename (size = ${size}Kb, deleted = $datetime)"
    fi
    index=$(($index + 1))
  done
  echo -e "$reset"

  echo -n "Which version of $1 should I restore ('0' to quit)? [1] :"
  read desired
  if [ ! -z "$(echo $desired | sed 's/[[:digit:]]//g')" ] ; then
    echo -e "$redf $0: Restore canceled by user: invalid input." >&2
    exit
  fi

  if [ ${desired:=1} -ge $index ] ; then
    echo -e "$0: Restore canceled by user: index value too big. $reset" >&2
    exit 1
  fi

  if [ $desired -lt 1 ] ; then
    echo -e "$redf $0: Restore canceled by user. $reset" >&2
    exit 1
  fi

  restore="$(ls -td1 *"$1" | sed -n "${desired}p")"

  if [ -e "$dest/$1" ] ; then
    echo -e "$redf '$1' already exists in this directory. Cannot   overwrite. $reset" >&2
    exit 1
  fi

  echo -n "Restoring file '$1' ..."
  $move "$restore" "$dest/$1"
  echo "done."

  echo -n "Delete the additional copies of this file? [y] "
  read answer

  if [ ${answer:=y} = "y" ] ; then
    $realrm -rf *"$1"
    echo "Deleted."
  else
    echo "Additional copies retained."
  fi
else
  if [ -e "$dest/$1" ] ; then
    echo -e "$redf '$1' already exits in this directory. Cannot overwrite. $reset" >&2
    exit 1
  fi

  restore="$(ls -d *"$1")"

  echo -n "Restoring file '$1' ..."
  $move "$restore" "$dest/$1"
  echo "Done."
fi

exit 0
