# Go Interface Type

## trap

```go
// 可以将任意对象赋值给 interface 变量
var v interface{}
v = true
v = 0
v = "Hello"

// 但是不能调用任何方法, 因为 v 中未声明任何方法
// 接口变量只能调用接口中声明的方法
var s io.Writer = os.Stdout
s.Read([]byte("")) // 编译错误 s.Read undefined (type io.Writer has no field or method Read)



```

## 关于类型持有方法

对于每一个命名过的具体类型 `T`, `T` 的一些方法的接收者是 `T` 本身然而另一些则是 `*T`.
在 `T` 类型的参数上调用一个 `*T` 的方法是合法的, 只要这个参数是一个变量,
编译器会隐式的获取它的地址(但是不能在无法寻址的 `T` 类型对象上调用 `*T` 的方法).
但这仅仅是一个语法糖, `T` **并不不拥有** `*T` 的方法. 如下所示:

```go
type T struct { value int }

func (t T) fun_1() int { return t.value }

func (t *T) fun_2() int { return t.value }

var _ = T{3}.fun_1() // 正常运行
var _ = T{3}.fun_2() // 编译错误, fun_2 is not in method set of T

var t = T{3}
t.fun_2() // 正常运行

/* --------------------------- */

type Writer struct {}

func (w *Writer) Write(p []byte) (int, error) {
    return 0, nil
}

var w Writer = Writer{}

var _ io.Writer = w // 编译错误, cannot use w (variable of type Writer) as io.Writer value in variable declaration: missing method Write

var _ io.Writer = &w // 正常运行

```

## 类型断言

```go
/*
基本语法1:
f := x.(T)
x 为接口类型, T 可以为接口类型也可以为具体类型

当 T 为具体类型时:
如果 x 的动态类型为 T, 则 x.(T) 返回 T, 否则会抛出 panic

当 T 为接口类型时:
如果 x 的动态类型实现了 T 中声明的所有方法, 则返回 T 类型. 即 f 只能使用 T 中声明的方法.

基本语法2:
f, ok := x.(T) // 不会抛出 panic, 断言失败 ok 为 false.
*/

var w io.Writer
w = os.Stdout
rw := w.(io.ReadWriter) // success: *os.File has both Read and Write
rw.Close // 编译错误, rw.Close undefined (type io.ReadWriter has no field or method Close)
f := w.(*os.File) // type(f) == *os.File
```
