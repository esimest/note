# Golang OOP

## 方法隐式调用

前提:

```go
type Point struct{ X, Y float64 }

func (p Point) Distance(q Point) float64 {
	return math.Hypot(p.X-q.X, p.Y-q.Y)
}

func (p *Point) ScaleBy(factor float64) {
	p.X *= factor
	p.Y *= factor
}

p := Point{1, 2}
pptr := &p
```

**在每一个合法的方法调用表达式中, 也就是下面三种情况里的任意一种情况都是可以的**:

```go
// 1. 方法的实际参数和形式参数的类型是一样的, 如:
Point{1, 2}.Distance(q)
pptr.ScaleBy(2)

// 2. 实参是的类型是 Point, 形参的类型是 `*Point`. 编译器会隐式的获取变量的地址:
p.ScaleBy(3) // (&p).ScaleBy(3)

// 3. 实参的类型是 `*Point`, 形参的类型是 `Ponit`. 编译器会隐式的获取指针指向的变量:
pptr.Distance(q) // (*pptr).Distance(q)
```

## 方法接收者(Reciver)

- 在现实的程序里, 一般会约定如果类有一个指针作为接收器的方法, 那么该类的所有方法都必须有一个指针接收器;
- 在声明方法时，如果一个类型名本身是一个指针的话，是不允许其出现在接收器中的;
- 方法的接收者为类型本身时, 调用方法如同函数调用一样, 传入的是对象的拷贝;
- 方法的接收者为类型指针时, 调用方法时, 传入的是对象的指针;

```go
type Point struct{ X, Y float64 }

// 由于方法的接收者是 Point 所以 p.X, p.Y 不会改变
func (p Point) ScaleBy(factor float64) {
	p.X *= factor
	p.Y *= factor
}

func geometry() {
    var p = Point{3.3, 4.4}
    p.ScaleBy(7.7)
	fmt.Println(p.X, p.Y)
}
```

```go
...
// 由于方法的接收者是 *Point 所以 p.X, p.Y 的值会改变
func (p *Point) ScaleBy(factor float64) {
	p.X *= factor
	p.Y *= factor
}

func geometry() {
    var p = Point{3.3, 4.4}
    p.ScaleBy(7.7)
	fmt.Println(p.X, p.Y)
}
```

## 类型拷贝

如果类型 T 的所有方法都是用 T 类型自己来做接收器(而不是*T), 那么拷贝这种类型的实例就是安全的, 调用他的任何一个方法也就会产生一个值的拷贝.
比如time.Duration的这个类型, 在调用其方法时就会被全部拷贝一份, 包括在作为参数传入函数的时候;

但是如果一个方法使用指针作为接收器, 你需要避免对其进行拷贝, 因为这样可能会破坏掉该类型内部的不变性.
比如你对 bytes.Buffer 对象进行了拷贝, 那么可能会引起原始对象和拷贝对象只是别名而已.
但实际上其指向的对象是一致的, 紧接着对拷贝后的变量进行修改可能会有让你意外的结果.

## nil

nil 是所有复合类型的零值, 在声明 T 类型的变量没有赋值时, 变量 == nil.
**但是此时并没有给该变量分配空间(即没有初始化), 因此无法更新该变量的值**.

## 成员函数

模块开发者可以通过方法提供成员函数的默认实现.
用户也可以实例化结构体时提供自己的实现, 对默认实现进行覆盖.