#!/bin/bash
# imgcache_update.sh -- 快速更新 imgcache, 不更新客制化包

function do_command(){
  # 执行命令，并检查命令是否执行成功
  # 执行成功正常退出
  # 如果失败，则报错然后结束进程
  # command: 要执行的命令
  # message: 执行过程中发出的消息

  command="$1"
  message="$2"

  echo "【command】: ${message}"
  ${command}

  if [ $? -eq 0 ]; then
    echo "【Success】: ${message}"
    return 0
  else
    echo "【Failed】: ${message}"
    exit -1
  fi
}

function check_update(){
  # 检查更新后的 imgcache 是否功能可用
  # 如果功能可用，正常退出
  # 如果不可用，回退后退出

  echo "【command】: check new imgcache"
    curl -H "Host: imgcache.ccb.com" http://127.0.0.1/open/qcloud/css/global.css > /dev/null 2>&1

  if [ $? -eq 0 ]; then
    echo "【Success】: check new imgcache"
    return 0
  else
    echo "【Failed】: check new imgcache, turn to old imgcache"
    rm -f /data/imgcache
    ln -s ${backup_path} /data/imgcache
    return 0
  fi
}

# main
#########################

if [ $# != 1 ]; then
  echo "格式：sh imgcache_update.sh  package_path"
  exit
fi

package_path="$1"
dest_path="/data/imgcache_v333_$(date +%Y%m%d)"
backup_path="/data/imgcache_v331_$(date +%Y%m%d)"

if [ ! -d ${backup_path} ]; then
  do_command "mkdir ${backup_path}" "make backup directory ${backup_path}"
  do_command "cp -r /data/imgcache/* ${backup_path}/" "backup imgcache"
fi

do_command "tar -zxf ${package_path} -C /tmp" "unpress imgcache.tar.gz"

do_command "mv /tmp/imgcache ${dest_path}" "move /tmp/imgcache to ${dest_path}"

do_command "cp -rf /data/imgcache/customize ${dest_path}/customize/" "copy /data/imgcache/customize to ${dest_path}/customize/"

do_command "rm -f /data/imgcache" "remove old link"
do_command "ln -s ${dest_path} /data/imgcache" "link /data/imgcache to ${dest_path}"

# check_update

exit
