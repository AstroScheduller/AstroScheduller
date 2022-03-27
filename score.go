package main

func score_get_best(obsObj obs, objects []src_obj, sortedObjs [][]src_obj) []src_obj {
	type score struct {
		score float64
		key   int
	}

	bestScore := score{-1, -1}

	for i := 0; i < len(sortedObjs); i++ {
		thisScore := score_scoring(obsObj, objects, sortedObjs[i])
		if thisScore > bestScore.score {
			bestScore.score = thisScore
			bestScore.key = i
		}
	}

	// if best score is -1, then there is no solution
	if bestScore.key == -1 {
		return nil
	}

	//if bestScore.key < 0 {
	//	fmt.Errorf("ERROR: No best solution found.")
	//	u_exit("NO VALID SCHEDULE FOUND.")
	//}

	//fmt.Println(bestScore.key)
	//return []src_obj{}
	return sortedObjs[bestScore.key]
}

func score_scoring(obsObj obs, objects []src_obj, sortedObj []src_obj) float64 {
	score := float64(0)

	durationTotal := float64(0)  // Amount of time ultilized
	gapLengthTotal := float64(0) // Length of gaps
	for i := 0; i < len(sortedObj); i++ {
		durationTotal = durationTotal + float64(sortedObj[i].Schedule.Duration[1]-sortedObj[i].Schedule.Duration[0])
		gapLengthTotal = gapLengthTotal + float64(sortedObj[i].Schedule.Gap)
	}

	if gapLengthTotal <= 1 {
		gapLengthTotal = 1
	}

	score = score + ((durationTotal)/float64(obsObj.Duration.End-obsObj.Duration.Begin))*10
	score = score + (1/gapLengthTotal)*10

	return score
}
