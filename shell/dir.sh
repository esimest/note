#!/bin/bash
# dir.sh -- Pretends we're the dir command in DOS and displays the contents
#   of the specified file, accepting some of the standard dir flags

function usage()
{
cat << EOF >&2
    Usage: $0 [DOS flags] directory or directories
    Where:
    /D        sort by columns
    /H        show help for this shell script
    /OD       sort by olddest to newest
    /O-D      sort by newest to olddest
    /P        pause after each screenful of information
    /S        recursive listing
    /W        use wide listing format
EOF
exit 1
}

####################
#### MAIN BLOCK

postcmd=""
flags=""

while [ $# -gt 0 ] ; do
    case $1 in
    /D         ) flags="$flags -x"    ;;
    /H         ) usage                ;;
    /[NQW]     ) flags="$flags -l"     ;;
    /OD        ) flags="$flags -rt"    ;;
    /O-D       ) flags="$flags -t"     ;;
    /P         ) postcmd="more"        ;;
    /S         ) flags="$flags -s"     ;;
              *)
    esac
    shift
done

if [ ! -z "$postcmd" ] ; then
    ls $flags "$@" | $postcmd
else
    ls $flags "$@"
fi

exit 0