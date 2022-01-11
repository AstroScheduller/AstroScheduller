package main

import (
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

		AltAz[i][0] = math.Asin(math.Sin(object.Dec/180*math.Pi)*math.Sin(telescope.Latitude/180*math.Pi)+math.Cos(object.Dec/180*math.Pi)*math.Cos(telescope.Latitude/180*math.Pi)*math.Cos(thisHourAngle/180*math.Pi)) / math.Pi * 180
		AltAz[i][1] = math.Acos((math.Sin(object.Dec/180*math.Pi)-math.Sin(AltAz[i][0]/180*math.Pi)*math.Sin(telescope.Latitude/180*math.Pi))/(math.Cos(AltAz[i][0]/180*math.Pi)*math.Cos(telescope.Latitude/180*math.Pi))) / math.Pi * 180

		if math.Sin(thisHourAngle) > 0 {
			AltAz[i][1] = 360 - AltAz[i][1]
		}
	}

	return AltAz
}

/**
* coord_sun_object: Get RA/Dec of the Sun (Error within 3 deg.)
* Reference: http://www.stargazing.net/kepler/sun.html.
 */
func coord_sun_object(timestamp int64) src_obj {
	var sunObj src_obj

	// Find the days before/after J2000.0 (d)
	d := timeTimestamp2J2000Days(timestamp)

	// Find the Mean Longitude (L) of the Sun
	L := coord_deg_range(280.461 + 0.9856474*d)

	// Find the Mean anomaly (g) of the Sun
	g := coord_deg_range(357.528 + 0.9856003*d)

	// Find the ecliptic longitude (lambda) of the sun
	lambda := L + 1.915*math.Sin(g) + 0.020*math.Sin(2*g)

	// Find the obliquity of the ecliptic plane (epsilon)
	epsilon := 23.439 - 0.0000004*d

	// Find the Right Ascension (alpha) and Declination (delta) of the Sun
	lambda = 134.97925
	epsilon = 23.439351
	Y := math.Cos(epsilon/180*math.Pi) * math.Sin(lambda/180*math.Pi)
	X := math.Cos(lambda / 180 * math.Pi)

	a := math.Atan(Y/X) / math.Pi * 180

	alpha := a
	if X < 0 {
		alpha = a + 180
	} else if Y < 0 && X > 0 {
		alpha = a + 360
	}

	delta := math.Asin(math.Sin(epsilon/180*math.Pi)*math.Sin(lambda/180*math.Pi)) / math.Pi * 180

	sunObj.Identifier = "SUN"
	sunObj.Ra = alpha
	sunObj.Dec = delta
	sunObj.Duration = 0
	sunObj.Rises = [][2]int64{}

	return sunObj
}

func coord_deg_range(degree float64) float64 {
	if degree > 360 {
		degree = degree - math.Floor(degree/360)*360
	} else if degree < 0 {
		degree = degree + (math.Floor(degree/-360)+1)*360
	}

	return degree
}
