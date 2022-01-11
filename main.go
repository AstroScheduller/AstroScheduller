package main

import (
	"fmt"
	"math"
	"os"
	"time"
)

func main() {
	startTime := time.Now().UnixNano()
	fmt.Println("_______       _____")
	fmt.Println("___    |________  /_____________")
	fmt.Println("__  /| |_  ___/  __/_  ___/  __ \\")
	fmt.Println("_  ___ |(__  )/ /_ _  /   / /_/ /")
	fmt.Println("/_/  |_/____/ \\__/ /_/    \\____/")
	fmt.Println("")
	fmt.Println("________     ______      _________      ___________")
	fmt.Println("__  ___/________  /____________  /___  ____  /__  /____________")
	fmt.Println("_____ \\_  ___/_  __ \\  _ \\  __  /_  / / /_  /__  /_  _ \\_  ___/")
	fmt.Println("____/ // /__ _  / / /  __/ /_/ / / /_/ /_  / _  / /  __/  /")
	fmt.Println("/____/ \\___/ /_/ /_/\\___/\\__,_/  \\__,_/ /_/  /_/  \\___//_/")
	fmt.Println("")
	fmt.Println("_________")
	fmt.Println("__  ____/_____")
	fmt.Println("_  / __ _  __ \\")
	fmt.Println("/ /_/ / / /_/ /")
	fmt.Println("\\____/  \\____/")
	fmt.Println("")

	fmt.Printf("Initializing...")
	initialize()
	//test()
	list_load_from_file(importPath)
	rises_get(loadedObsParam, loadedSrcParam)
	fmt.Printf("\rInitializing... Done.   \n")

	fmt.Printf("Scheduling...")
	if loadedObsParam.Escape.Sun != 0 {
		loadedObsParam.Escape.Sun = loadedObsParam.Escape.Sun + 3 // For the reason that estimated AltAz overall has an 3 degree error.
	}
	bestSchedule := score_get_best(loadedObsParam, loadedSrcParam.Objects, sort_get(loadedObsParam, loadedSrcParam.Objects))
	fmt.Printf("\rScheduling... Done.   \n")

	fmt.Printf("Exporting...")
	list_export(loadedObsParam, bestSchedule, exportPath)
	fmt.Printf("\rExporting... Done.   ")

	fmt.Println()
	fmt.Println()
	fmt.Println("=================")
	fmt.Println("The schedule has been successfully generated. (v0.9.1 Dev.)")
	fmt.Println("AstroSchedullerGo is released as an open source project under the MIT license. See https://github.com/xiawenke/AstroSchedullerGo for more information.")
	fmt.Println("")
	endTime := time.Now().UnixNano()
	fmt.Println("Completed: ", float64(endTime-startTime)/math.Pow(10, 9), "sec.")
}

func initialize() bool {

	Config_RisesSearchStep = 300
	FloatConfig_RisesSearchStep = float64(Config_RisesSearchStep)
	Config_SortSearchStep = 300
	FloatConfig_SortSearchStep = float64(Config_SortSearchStep)
	Config_SunSearchStep = 21600
	FloatConfig_SortSearchStep = float64(Config_SunSearchStep)

	if len(os.Args) >= 3 {
		importPath = os.Args[1]
		exportPath = os.Args[2]
	}

	return true
}

func test() {
	//fmt.Println("Testing...")

	//importPath = "./tests/psr_list_debug_short.xml"
	//importPath = "./tests/psr_list_debug.xml"
	importPath = "./tests/psr_list_long.xml.gitignore"
	exportPath = "./tests/export.xml"

	/**
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
	**/

	//fmt.Println("Testing... Done.")
	//os.Exit(0)
}
