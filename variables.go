package main

import "encoding/xml"

/********************/
/** TYPE STRUCTURE **/
/********************/
type obs_dur struct {
	Begin int64 `xml:"begin"`
	End   int64 `xml:"end"`
}

type obs_tele struct {
	Latitude  float64       `xml:"latitude"`
	Longitude float64       `xml:"longitude"`
	Altitude  float64       `xml:"altitude"`
	Velocity  obe_tele_velo `xml:"velocity"`
}

type obe_tele_velo struct {
	Ra  float64 `xml:"ra"`
	Dec float64 `xml:"dec"`
}

type obs_elev struct {
	Minimal float64 `xml:"minimal"`
	Maximal float64 `xml:"maximal"`
}

type obs_escp struct {
	Sun      float64 `xml:"sun"`
	SunAltAz [][]float64
}

type obs struct {
	//XMLName   xml.Name `xml:"observation"`
	Duration  obs_dur  `xml:"duration"`
	Telescope obs_tele `xml:"telescope"`
	Elevation obs_elev `xml:"elevation"`
	Escape    obs_escp `xml:"escape"`
}

type src_obj struct {
	Identifier string  `xml:"identifier"`
	Ra         float64 `xml:"ra"`
	Dec        float64 `xml:"dec"`
	Duration   int64   `xml:"duration"`
	Weight     float64 `xml:"weight"`
	Important      int     `xml:"important"`
	Rises      [][2]int64
	SortMark   bool
	Schedule   schedule
}

type src struct {
	//XMLName xml.Name `xml:"sources"`
	Objects []src_obj `xml:"object"`
}

type obs_config struct {
	XMLName     xml.Name `xml:"scheduller"`
	Observation obs      `xml:"observation"`
	Sources     src      `xml:"sources"`
}

type timestamp_obj struct {
	Timestamp int64
	Year      int64
	Month     int64
	Day       int64
	Hour      int64
	Minute    int64
	Second    int64
	YearDay   int64
}

type schedule struct {
	Scheduled bool
	Key       int
	Duration  [2]int64
	Gap       int64 //Gap from last object to this object
}

/**********************/
/** GLOBAL VARIABLES **/
/**********************/
var loadedObsParam obs
var loadedSrcParam src
var importPath string
var exportPath string

// var duration = [2]int64{1647284400, 1647294400}
// var telescope = [3]float64{45.52, -82.681944, 0} //[Lat., Lon., Hei.] TM Tele.

/**********************/
/** CONFIG VARIABLES **/
/**********************/
var Config_RisesSearchStep int64
var FloatConfig_RisesSearchStep float64
var Config_SortSearchStep int64
var FloatConfig_SortSearchStep float64
var Config_SunSearchStep int64
var FloatConfig_SunSearchStep float64

//var Config_RisesSearchStep int64
