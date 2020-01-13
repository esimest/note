package main

func main() {
	var count int = 10

	println("count: \t value of [", count, "]\t Addr of[", &count, "]")

	increment(&count)

	println("count: \t value of [", count, "]\t Addr of[", &count, "]")
}

func increment(inc *int) {
	*inc++
	println("inc:\t value of [", *inc, "]\t Addr of[", inc, "]")
}

/*
count:   value of [ 10 ]         Addr of[ 0xc00002ff48 ]
inc:     value of [ 11 ]         Addr of[ 0xc00002ff40 ]
count:   value of [ 10 ]         Addr of[ 0xc00002ff48 ]
*/
