#!/bin/bash
#images_update.sh -- 批量更新 dcoker 镜像

function load_images(){
  # 进入到镜像包所在目录
  # 并依次 load 镜像至本地仓库

  img_dir="$1"
  cd ${img_dir}
  # ls | xargs -n1 docker load -i
  for file in $(ls); do
    docker load -i ${file}  > /dev/null 2>&1

    if [ ! -z $? ]; then
      echo "load ${file} failed!" >&2
    else
      echo "${file} load success!"
    fi
  done
}

function push_images(){
  # 进入到镜像包所在目录
  # 使用 dokcer images 查看对应更新的镜像，
  # 并通过信息构造新的 img_name，然后 push 到远程仓库

  img_dir="$1"
  cd ${img_dir}

  for file in $(ls); do
    tag=$(echo ${file} | cut -d. -f1)
    img_info=$(docker images | grep ${tag})
    img_info=${img_info//\\t/ /}

    img_name=$(echo ${img_info}| cut -d' ' -f1)":"$(echo ${img_info}| cut -d' ' -f2)
    docker push ${img_name}  > /dev/null 2>&1
    if [ ! -z $? ]; then
      echo "${img_name} push failed!" >&2
    else
      echo "${file} push success!"
    fi
  done
}

# main
#########################

if [ $# != 1 ]; then
  echo "格式：shimages_update.sh img_dir"
  exit
fi

img_dir="$1"

load_images ${img_dir}

push_images ${img_dir}
