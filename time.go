package main

import "time"

/**
* TimeObject: Format timestamp to time object.
* In: int64 timestamp
* Out: [5]int64 timestamp, YearDay, Hour, Minute, Second
 */
func timeObject(timestamp int64) [5]int64 {
	timestampImported := time.Unix(timestamp, 0).UTC()

	return [5]int64{timestamp,
		int64(timestampImported.YearDay()),
		int64(timestampImported.Hour()),
		int64(timestampImported.Minute()),
		int64(timestampImported.Second())}
}

/**
* TimePlus: Plus time object to seconds
* In: [5]int64 timeObject, int64 seconds
* Out: [5]int64 timeObject
 */
func timePlus(timeObj [5]int64, seconds int64) [5]int64 {
	return timeObject(timeObj[0] + seconds)
}

func timeTimestamp2J2000Days(timestamp int64) float64 {
	return (float64(timestamp) - 946700820) / 86459.1780821918
}
