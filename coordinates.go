package main

import (
	"fmt"
	"math"
	"time"
)

/**
* coord_siderial_time: Calculate LST (2nd)
* Reference: http://www.stargazing.net/kepler/altaz.html#:~:text=RA%20%3D%2016.695%20%2A%2015%20%3D%20250.425%20degrees,HA%20and%20DEC%20to%20the%20ALT%20and%20AZ.
 */
func coord_siderial_time2(d, UT, long float64) float64 {
	return coord_deg_range(100.46 + 0.985647*d + long + 15*UT)
}

/**
* coord_siderial_time: Calculate LST
* Adopted from https://github.com/jhaupt/Sidereal-Time-Calculator/blob/master/SiderealTimeCalculator.py
 */
func coord_siderial_time(timestamp, Long float64) float64 {
	//hemisphere := 'W'
	//if Long > 0 {
	//	hemisphere = 'E'
	//}
	LongDeg := math.Floor(Long)
	LongMin := (Long - LongDeg) * 60
	LongSec := (LongMin - math.Floor(LongMin)) * 60
	LongMin = math.Floor(LongMin)
	LongSec = math.Floor(LongSec)

	goTimeObj := time.Unix(int64(timestamp), 0).UTC()
	MM := math.Floor(float64(goTimeObj.Month()))
	DD := math.Floor(float64(goTimeObj.Day()))
	YY := math.Floor(float64(goTimeObj.Year()))
	hh := math.Floor(float64(goTimeObj.Hour()))
	mm := math.Floor(float64(goTimeObj.Minute()))

	mm = mm / 60
	UT := hh + mm

	JD := (367 * YY) - math.Floor((7*(YY+math.Floor((MM+9)/12)))/4) + math.Floor((275*MM)/9) + DD + 1721013.5 + (UT / 24)

	GMST := 18.697374558 + 24.06570982441908*(JD-2451545)
	GMST = math.Mod(GMST, 24)
	GMSTmm := (GMST - math.Floor(GMST)) * 60
	GMSTss := (GMSTmm - math.Floor(GMSTmm)) * 60
	//GMSThh := math.Floor(GMST)
	GMSTmm = math.Floor(GMSTmm)
	GMSTss = math.Floor(GMSTss)

	Long = Long / 15
	LST := GMST + Long

	if LST < 0 {
		LST = LST + 24
	}

	return LST * 15
}

//func coord_alt_az()

func coordinate(ra, dec float64) [2]float64 {
	return [2]float64{ra, dec}
}

/**
* AltAz: Transform RaDec to AltAz
* Reference: http://www.stargazing.net/kepler/altaz.html#:~:text=RA%20%3D%2016.695%20%2A%2015%20%3D%20250.425%20degrees,HA%20and%20DEC%20to%20the%20ALT%20and%20AZ.
 */
func AltAz(object src_obj, timestamps []int64, telescope obs_tele) [][2]float64 {
	//Float_obsTimeBeg := float64(obsTime.Begin)
	//slices := int(obsTime.End-obsTime.Begin) / Config_AltAzStep
	//timestamps := make([]float64, slices)
	AltAz := make([][2]float64, len(timestamps))
	//var AltAz [][2]float64

	for i := 0; i < len(timestamps); i++ {
		//timestamps[i] = Float_obsTimeBeg + float64(i)*FloatConfig_AltAzStep
		// LST
		//thisLST := coord_siderial_time(timestamps[i], telescope[1])
		//thisLST := coord_siderial_time2(timeTimestamp2J2000Days(int64(timestamps[i])), float64(time.Unix(int64(timestamps[i]), 0).UTC().Hour()), telescope.Longitude)
		thisLST := coord_siderial_time(float64(timestamps[i]), telescope.Longitude)
		thisHourAngle := coord_deg_range(thisLST - object.Ra)
		fmt.Println(thisLST)

		AltAz[i][0] = math.Asin(math.Sin(object.Dec/180*math.Pi)*math.Sin(telescope.Latitude/180*math.Pi)+math.Cos(object.Dec/180*math.Pi)*math.Cos(telescope.Latitude/180*math.Pi)*math.Cos(thisHourAngle/180*math.Pi)) / math.Pi * 180
		AltAz[i][1] = math.Acos((math.Sin(object.Dec/180*math.Pi)-math.Sin(AltAz[i][0]/180*math.Pi)*math.Sin(telescope.Latitude/180*math.Pi))/(math.Cos(AltAz[i][0]/180*math.Pi)*math.Cos(telescope.Latitude/180*math.Pi))) / math.Pi * 180

		if math.Sin(thisHourAngle) > 0 {
			AltAz[i][1] = 360 - AltAz[i][1]
		}
	}

	return AltAz
}

func coord_deg_range(degree float64) float64 {
	if degree > 360 {
		degree = degree - math.Floor(degree/360)*360
	} else if degree < 0 {
		degree = degree + (math.Floor(degree/-360)+1)*360
	}

	return degree
}
