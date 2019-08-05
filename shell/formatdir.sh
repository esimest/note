#!/bin/bash

# formatdir -- Outputs a directory listing in a friendly and useful format
# Note that need to ensure "scriptbc" is in your current path
#   because it's invoked within the script more than once.

.ansi_color.sh

scriptbc=$(which scriptbc)

# Function to format size in KB to KB, MB, or GB for more readable output
readablesize(){
  if [ $1 -ge 1048576 ] ; then
    echo "$(${scriptbc} -p 2 $1 / 1048576)GB"
  elif [ $1 -ge 1024 ] ; then
    echo "$(${scriptbc} -p 2 $1 / 1024)MB"
  else
    echo "${1}KB"
  fi
}

#####################
## MAIN CODE

if [ $# -gt 1 ] ; then
  echo -e "${redf}Usage: $0 [dirname]${reset}" > &2
  exit 1
elif [ $# -eq 1 ] ; then  # Specified a directory other than the current one?
  cd "$@"
  if [ $? -ne 0 ] ; then
    exit 1
  fi
fi

for file in *
do
  if [ -d "${file}" ] ; then
    size=$(ls "$file" | wc -l | sed 's/[^[:digit:]]//g')
    if [ $size -eq 0 ] ; then
      echo "${file} (${size} entry)|"  # 行尾的竖线留给 awk 使用
    else
      echo "${file} (${size} entries)|"
    fi
  else
    size="$(ls -sk "${file}" | awk '{print $1}'"
    echo "${file} ($readablesize ${size}))|"
  fi
done | \  # 将 for 循环的所有输出结果统一处理
  sed 's/ /^^^/g' | \  # xargs 默认以 空格 换行 ... 为分隔符，所以需要转换
  xargs -n 2  | \
  sed 's/\^\^\^/ /g' | \
  awk -F\| '{ printf "%-29s %-39s\n", $1, $2}'  # 反斜杠竖线，获取转义字符的真实值

exit 0