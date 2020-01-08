# Cobra

Cobra 是一个用于编写命令行工具的 Golang 库.

## Concept

Cobra 有三个核心概念 `Command`, `Flag`, `Argument/args`

```shell
kubectl get pod --watch

# kubectl --> rootCommand

# get --> Command

# pod --> Argument/args

# watch --> Flag

```

## 项目组成

### Cobra init

1. 在 `GO_PATH` 外创建一个 `my_calc` 目录并执行 `go mod init my_calc` 创建项目.

2. 在 `my_calc` 目录中使用 `cobra init --pkg-name my_calc` 初始化 cobra 项目.

项目结构为:

```shell
[root@my_calc#] ls -R
.:
cmd  go.mod  go.sum  LICENSE  main.go
./cmd:
root.go
```

`main.go(可以自定义为别的名字)` 为程序的入口. 主要包含:

```go
func main() {
	cmd.Execute()
}
```

`cmd/roog.go` 中定义了根命令`rootCmd`.以及初始化函数`init`,
项目中并没有显示的调用 `cmd.init` 函数, 但是通过调试发现 init 执行在
`main.main` 之前. 用于初始化命令的 Flag.

```go
// 通过在每个函数中添加一条打印语句来确定函数的执行顺序
//main.go
func main() {
	fmt.Println("func main.main")
	cmd.Execute()
}

//  cmd/root.g
func Execute() {
	fmt.Println("func cmd.Execute")
	...
	}
}

func init() {
	fmt.Println("func cmd.init")
    cobra.OnInitialize(initConfig)
    ...
}
```

```shell
# 执行结果
[root@my_calc#] go run main.go
func cmd.init
func main.main
func cmd.Execute
...
```

### Run

`Run/RunE` 为 `cobra.Command` 主要函数, 用于执行命令的逻辑代码.
大部分简易的 cobra 项目直接实现这个方法就行了.

### Flag

Flag 用于扩展命令的功能. 主要有全局Flag(PersistentFlags) 和局部Flag(Flag).

### initConfig

initConfig 函数用于从配置文件或环境变量中加载项目的配置, 函数中使用 `viper` 库(用于加载配置的 golang 库).

## Code

### 添加子命令

为 `my_calc` 命令添加子命令 `add`, 并通过实现简单的命令行加法功能具体介绍 cobra 的用法.

```shell
# 添加子命令 add
cobra add add # 此命令会在 cmd 目录下增加 add.go 文件.
```

```go
// add.go 内容和 root.go 类似, 也会实例化一个 cobra.Command
var addCmd = &cobra.Command{
	Use:   "add",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("add called") // 默认的行为是打印处 'add called'
	},
}

// 通过修改 Run 函数的内容来实现自定义命令的行为


func addInt(args []string) {
	var sum int
	for _, ival := range args {
		itemp, err = strconv.Atoi(ival)

		if err != nil {
			fmt.Println(err)
		}
		sum += itemp
	}
	fmt.Printf("Sum of %s is %d", args, sum)
}

...
	Run: func(cmd *cobra.Command, args []string) {
		addInt(args)
	},
...
```

```shell
# 执行结果为
[root@my_calc#] go run main.go add 3 4 5
Sum of [3 4 5] is 12
```

### 命令添加 Flag 扩展命令功能

为 add 命令添加 `-f` flag 在不影响 `add` 命令原来功能的情况下, 实现命令行小数的加法.

```go
// init 函数中填加 flag
func init() {
	rootCmd.AddCommand(addCmd)

    addCmd.Flags().BoolP("float", "f", false, "Add Floating Numbers")
    ...
}

// 添加 addFlat 函数
func addFloat(args []string) {
	var sum float64

	for _, fval := range args {
		// convert string to float64
		ftemp, err := strconv.ParseFloat(fval, 64)
		if err != nil {
			fmt.Println(err)
		}
		sum = sum + ftemp
	}
	fmt.Printf("Sum of floating numbers %s is %f", args, sum)
}

// 修改 Run 方法支持 addFloat
...
	Run: func(cmd *cobra.Command, args []string) {
		fstatus, _ := cmd.Flags().GetBool("float")

		if fstatus {
			addFloat(args)
		} else {
			addInt(args)
		}
    },
...
```

```shell
# 执行结果
[root@my_calc#] go run main.go add 3.3 4.5 -f
Sum of floating numbers [3.3 4.5] is 7.800000
```
