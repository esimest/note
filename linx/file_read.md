# 文件读取命令

## more/less

## cat

## head

## tail

## tee

> 读取标准输入，将内容同时输出至标准输出和文件

```shell
# 输出 "hello world" 并保存至 hello.txt
echo "hello world" | tee hello.txt

# 输出 "this is esime" 并追加至 hello.txt
echo "this is esime" | tee -a hello.txt

# -i 选项，忽略中断

# 等待用户输入，输出至标准输出，并保存之 hello.txt
tee hello.txt 回车

```
