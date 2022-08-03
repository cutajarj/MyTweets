package main

func PrimeFactors(number int) {
	for p := 2; number >= p*p; {
		if number%p == 0 {
			println(p)
			number /= p
		} else {
			p += 1
		}
	}
	println(number)
}

func main() {
	PrimeFactors(100)
}
