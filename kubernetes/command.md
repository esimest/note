# Kubernetes Commands

## Kubernetes 主要功能

1. 服务发现与负载均衡(Service)

2. 容器自动装箱(Schduler)

3. 存储编排(Volume)

4. 自动容器恢复(Controller)

5. 自动发布与回滚(Rollout)

6. 配置与密文管理(ConfigMap, Secret)

7. 批量执行(Job)

8. 水平伸缩(Scale)

## 常用 kubectl 命令

```shell
# 执行 yaml 文件
kubectl apply -f ${yaml_file}

# 查看所有资源对象
kubectl api-resources

# 单个 pod 含有多个 container 时进入容器
kubectl exec -it ${pod_name} -c ${container_name} bash

# 进入容器
kubectl exec -it $(kubectl get po -n ${ns} |grep ${img_name} | awk 'NR==1{print $1}') -n ${ns} bash

# 批量执行命令
kubectl get pod | grep ${name} | xargs -n1 -i kubectl exec {} -- ${command}

# 命令行创建 svc
kubectl expose deploy ${deploy_name} --port=${dest_port} --target-port=${expose_port}

# node 打标签
kubectl label nodes ${node_name} ${key}=${value}

# 覆盖 node 上的标签
kubectl label nodes ${node_name} ${key}=${value} --over-write

# 删除 node 上的标签
kubectl label no ${node_name} ${key}-

# 实时检测资源的变化
kubectl get --watch ${object}
kubectl get ${object} -w

# 过滤输出内容
kubectl get ${object} -o template --template={{.metadata.slefLink}}

# 访问 api-server 指定 url 路径
kubectl get --raw=${URL}
## 例
kubectl get --raw=/metrics
kubectl get --raw=/openapi/v2
kubectl get --raw=/
```

## 常用别名

```shell
alias kbad='kubectl get po -A -owide | awk "\$4 !~ /(Running)|(Completed)/"'
alias kd='kubectl delete'
alias ke='kubectl edit'
alias kg='kubectl get'
alias kgy='kubectl get -oyaml'
alias kga='kubectl get -A'
alias klogs='kubectl logs'
alias ks='kubectl describe'

function kgrep() {
  while getopts "n:" arg; do
    case ${arg} in
      n) namespace=${OPTARG}      ;;
    esac
  done
  shift $(( $OPTIND - 1 ))

  if [[ $# == 1 ]]; then
    kubectl get po -A -owide | grep $1
  elif [[ $# == 2 ]]; then
    if [[ ${namespace} == "" ]]; then
      kubectl get -A $1 -owide | grep $2
    else
      kubectl get -n${namespace} $1 -owide | grep $2
    fi
  else
    exit 1
  fi
}

function kin() {
  while getopts "n:c:" arg; do
    case ${arg} in
      n) namespace=${OPTARG}      ;;
      c) container=${OPTARG}      ;;
    esac
  done
  shift $(( $OPTIND - 1 ))

  namespace=${namespace:=default}

  if [[ ! ${container} == "" ]]; then
    kubectl exec -it -n${namespace} $1 -c ${container} sh
  else
    kubectl exec -it -n${namespace} $1 sh
  fi
}

function kdo() {
  while getopts "n:c:" arg; do
    case ${arg} in
      n) namespace=${OPTARG}      ;;
      c) container=${OPTARG}      ;;
    esac
  done
  shift $(( $OPTIND - 1 ))

  name=$1
  shift 1
  if [[ ! ${container} == "" ]]; then
    kubectl exec -n${namespace} ${name} -c${container} -- $*
  else
    kubectl exec -n${namespace} ${name} -- $*
  fi
}

```
