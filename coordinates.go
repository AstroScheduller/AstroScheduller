package main

import (
	"fmt"
)

func timeObject(timestamp int32) [7]int32 {
	year := (1970 + (timestamp / 31556952))
	month := ((timestamp % 31556952) / 2629746)
	day := (((timestamp % 31556952) % 2629746) / 86400)
	hour := ((((timestamp % 31556952) % 2629746) % 86400) / 3600)
	minute := (((((timestamp % 31556952) % 2629746) % 86400) % 3600) / 60)
	second := (((((timestamp % 31556952) % 2629746) % 86400) % 3600) % 60)

	return [7]int32{timestamp, year, month, day, hour, minute, second}
}

func coordinate(ra, dec float32) [2]float32 {
	return [2]float32{ra, dec}
}

func AltAz(coordObj [2]float32, obsTime [7]int32, location [3]float32) {
	fmt.Println(coordObj)
	fmt.Println(obsTime)
	fmt.Println(location)

}
