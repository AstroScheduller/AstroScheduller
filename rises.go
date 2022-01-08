package main

func rises_get(obsParam obs, srcParam src) src {
	for i := 0; i < len(srcParam.Objects); i++ {
		srcParam.Objects[i] = rises_search(obsParam, srcParam.Objects[i])
	}
	return srcParam
}

func rises_search(obsParam obs, objParam src_obj) src_obj {
	thisRise := [2]int64{-1, -1}

	for t := obsParam.Duration.Begin; t < obsParam.Duration.End; t = t + Config_RisesSearchStep {
		thisAltAz := AltAz(objParam, []int64{t}, obsParam.Telescope)[0]
		//fmt.Println(thisAltAz[0] > obsParam.Elevation.Minimal)
		//fmt.Println(thisAltAz[0] < obsParam.Elevation.Maximal)
		//fmt.Println(obsParam.Elevation.Minimal)
		if thisAltAz[0] > obsParam.Elevation.Minimal && thisAltAz[0] < obsParam.Elevation.Maximal {
			if thisRise[0] == -1 {
				thisRise[0] = t
			}
		} else {
			if thisRise[1] == -1 && thisRise[0] != -1 {
				thisRise[1] = t
				objParam.Rises = append(objParam.Rises, thisRise)
				thisRise = [2]int64{-1, -1}
			}
		}
	}

	if thisRise[0] != -1 && thisRise[1] == -1 {
		thisRise[1] = obsParam.Duration.End
		objParam.Rises = append(objParam.Rises, thisRise)
	}

	return objParam
}
