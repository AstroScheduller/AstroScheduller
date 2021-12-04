package main

import "fmt"

var duration = [2]uint32{1638568832, 1638578832}
var telescope = [3]float32{31, 121.9, 10} //[Lat., Lon., Hei.] TM Tele.

func main() {
	fmt.Println("TEST")
	timeObj := time(1638568832)
	coordObj := coordinate(0.1, -0.1)
	AltAz(coordObj, timeObj, telescope)
}
