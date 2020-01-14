package main

import "fmt"

type st struct {
	name string
	age  int
}

func main() {
	s1 := &st{"esimest", 32}

	func(s *st) {
		s.name = "Hello"
	}(s1)

	m := map[string]int{"hello": 3}

	hw()
	println(m["hello"])
	println(s1.name)
	fmt.Printf("%T", s1)
}

func hw() {
	println("hello wow...")
}
