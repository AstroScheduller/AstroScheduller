package main

import (
	"fmt"
)

func main() {
	fmt.Println("== SchedullerGo Dev Version ==")
	initialize()
	test()
	//timeObj := timeObject(duration[1])
}

func initialize() bool {
	fmt.Println("Initializing...")

	configInitialize()

	fmt.Println("Initializing... Done.")

	return true
}

func test() {
	fmt.Println("Testing...")

	fmt.Println("Testing List functions...")
	list_load_from_file("./tests/psr_list_long.xml")
	fmt.Println(loadedObsParam)
	fmt.Println(loadedSrcParam)
	fmt.Println()

	fmt.Println("Testing AltAz functions...")
	//coordObj := coordinate(144.95, 82.71666667)
	//AltAz(coordObj, loadedObsParam.Duration, loadedObsParam.Telescope)
	fmt.Println(AltAz(loadedSrcParam.Objects[0], []int64{1627171140}, loadedObsParam.Telescope))
	fmt.Println()

	fmt.Println("Testing Rises functions...")
	fmt.Println(rises_get(loadedObsParam, loadedSrcParam).Objects[0].Rises)
	fmt.Println()

	fmt.Println("Testing Sorting functions...")
	//fmt.Printf("%+v", sort_nearest(loadedSrcParam.Objects, 3))
	//fmt.Println(sort_get(loadedObsParam, loadedSrcParam.Objects))
	fmt.Println()

	fmt.Println("Testing Scoring functions...")
	bestObjectList := score_get_best(loadedObsParam, loadedSrcParam.Objects, sort_get(loadedObsParam, loadedSrcParam.Objects))
	fmt.Println()

	fmt.Println("Testing Export functions...")
	list_export(loadedObsParam, bestObjectList, "./export.xml")
	fmt.Println()

	for i := 0; i < len(loadedSrcParam.Objects); i++ {
		thisObj := loadedSrcParam.Objects[i]
		if thisObj.Ra == 280.186 {
			fmt.Println(thisObj.Identifier)
			loadedObsParam.Telescope.Latitude = 32.7015
			loadedObsParam.Telescope.Longitude = -109.891284
			fmt.Println(AltAz(thisObj, []int64{1627110000, 1627110000 + 7200*1, 1627110000 + 7200*2, 1627110000 + 7200*3, 1627110000 + 7200*4, 1627110000 + 7200*5, 1627110000 + 7200*6, 1627110000 + 7200*7, 1627110000 + 7200*8, 1627110000 + 7200*9, 1627110000 + 7200*10, 1627110000 + 7200*11, 1627110000 + 7200*12}, loadedObsParam.Telescope))
		}
	}

	fmt.Println("Testing... Done.")
}

func configInitialize() bool {
	Config_RisesSearchStep = 300
	FloatConfig_RisesSearchStep = float64(Config_RisesSearchStep)
	Config_SortSearchStep = 300
	FloatConfig_SortSearchStep = float64(Config_SortSearchStep)
	return true
}
