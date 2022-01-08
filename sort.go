package main

import (
	"math"
)

func sort_get(obsObj obs, objects []src_obj) [][]src_obj {
	var sortedObjects [][]src_obj

	// Discard objects that is not rising...
	for i := 0; i < len(objects); i++ {
		if len(objects[i].Rises) == 0 {
			objects = sort_discard_object(objects, i)
		}
	}

	for i := 0; i < len(objects); i++ {
		sortedObjects = append(sortedObjects, sort_objects(obsObj, sort_nearest(objects, i)))
	}

	return sortedObjects
}

func sort_objects(obsObj obs, objects []src_obj) []src_obj {
	time := obsObj.Duration.Begin
	sortedObj := []src_obj{}

	for {
		var thisSched schedule
		thisSched.Scheduled = false

		for i := 0; i < len(objects); i++ {
			thisGap := int64(0)
			if len(sortedObj) > 0 {
				thisGap = sort_gap_between(obsObj, sortedObj[len(sortedObj)-1], objects[i])
			} else {
				thisGap = time - obsObj.Duration.Begin
			}

			if sort_observable(objects[i], [2]int64{time, time + objects[i].Duration}) {
				thisSched.Scheduled = true
				thisSched.Key = i
				thisSched.Duration = [2]int64{time, time + objects[i].Duration}
				thisSched.Gap = thisGap
			}
		}

		// Shortest Rise: if the object has the shortest rise time and if can't be observed in the next search loop, it has higher priority.
		sRiseObjKey := sort_shortest_rise(objects)

		sRiseObjKeyGap := int64(0)
		if len(sortedObj) > 0 {
			sRiseObjKeyGap = sort_gap_between(obsObj, sortedObj[len(sortedObj)-1], objects[sRiseObjKey])
		} else {
			sRiseObjKeyGap = time - obsObj.Duration.Begin
		}

		if sort_observable(objects[sRiseObjKey], [2]int64{time, time + objects[sRiseObjKey].Duration}) {
			if thisSched.Scheduled {
				if !sort_observable(objects[sRiseObjKey], [2]int64{thisSched.Duration[1] + thisSched.Gap, thisSched.Duration[1] + thisSched.Gap + objects[sRiseObjKey].Duration}) {
					thisSched.Scheduled = true
					thisSched.Key = sRiseObjKey
					thisSched.Duration = [2]int64{time, time + objects[sRiseObjKey].Duration}
					thisSched.Gap = sRiseObjKeyGap
				}
			} else {
				if !sort_observable(objects[sRiseObjKey], [2]int64{time + Config_SortSearchStep, time + Config_SortSearchStep + objects[sRiseObjKey].Duration}) {
					thisSched.Scheduled = true
					thisSched.Key = sRiseObjKey
					thisSched.Duration = [2]int64{time, time + objects[sRiseObjKey].Duration}
					thisSched.Gap = sRiseObjKeyGap
				}
			}
		}

		if thisSched.Scheduled {
			objects[thisSched.Key].Schedule = thisSched
			sortedObj = append(sortedObj, objects[thisSched.Key])
			objects = sort_discard_object(objects, thisSched.Key)

			time = time + thisSched.Duration[1] - thisSched.Duration[0] + thisSched.Gap
			thisSched = schedule{}
		} else {
			time = time + Config_SortSearchStep
		}

		if time >= obsObj.Duration.End || len(sortedObj) == len(objects) {
			break
		}

	}

	return sortedObj
}

func sort_observable(object src_obj, duration [2]int64) bool {
	observable := false

	for i := 0; i < len(object.Rises); i++ {
		if object.Rises[i][0] <= duration[0] && object.Rises[i][1] >= duration[1] {
			observable = true
		}
	}

	// To-do: Escape Sun

	return observable
}

func sort_discard_object(objects []src_obj, discardKey int) []src_obj {
	processedObject := []src_obj{}

	for i := 0; i < len(objects); i++ {
		if i != discardKey {
			processedObject = append(processedObject, objects[i])
		}
	}

	return processedObject
}

/**
func sort_next_object(objects []src_obj) int {
	for i := 0; i < len(objects); i++ {
		if objects[i].SortMark != true {
			return i
		}
	}

	return -1
}
*/

func sort_nearest(objects []src_obj, i int) []src_obj {
	var nearest float64
	sortedObjs := []src_obj{}

	for i := 0; i < len(objects); i++ {
		objects[i].SortMark = false
	}

	for {
		sortedObjs = append(sortedObjs, objects[i])
		objects[i].SortMark = true

		if len(objects) == len(sortedObjs) {
			break
		}

		nearest = float64(-1)
		for k := 0; k < len(objects); k++ {
			if !objects[k].SortMark {
				thisDistance := sort_angle_distance(objects[i], objects[k])
				if thisDistance < nearest || nearest == float64(-1) {
					i = k
					nearest = thisDistance
				}
			}
		}
	}

	return sortedObjs
}

func sort_angle_distance(obj1 src_obj, obj2 src_obj) float64 {
	return math.Sqrt(math.Pow(obj1.Ra-obj2.Ra, 2) + math.Pow(obj1.Dec-obj2.Dec, 2))
}

func sort_shortest_rise(objects []src_obj) int {
	shortestKey := [2]int{-1, -1} // {riseTime, i}

	for i := 0; i < len(objects); i++ {
		thisRise := 0

		for a := 0; a < len(objects[i].Rises); a++ {
			thisRise = thisRise + int(objects[i].Rises[a][1]-objects[i].Rises[a][0])
		}

		if thisRise > int(shortestKey[0]) {
			shortestKey = [2]int{thisRise, i}
		}
	}

	return shortestKey[1]
}

func sort_gap_between(obsObj obs, object1 src_obj, object2 src_obj) int64 {
	t := [2]int64{int64(math.Abs((object1.Ra - object2.Ra) / obsObj.Telescope.Velocity.Ra)), int64(math.Abs((object1.Dec - object2.Dec) / obsObj.Telescope.Velocity.Dec))}

	if t[1] > t[0] {
		return t[1]
	}

	return t[0]
}
