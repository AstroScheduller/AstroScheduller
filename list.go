package main

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"os"
)

func list_load_from_file(filename string) bool {
	loaded_xml := list_load_xml(u_file_get_file_annotated(filename))
	loadedObsParam = loaded_xml.Observation
	loadedSrcParam = loaded_xml.Sources

	for i := 0; i < len(loadedSrcParam.Objects); i++ {
		if loadedSrcParam.Objects[i].Important != 1{
			loadedSrcParam.Objects[i].Important = 0
		}

		if loadedSrcParam.Objects[i].Weight > 1 || loadedSrcParam.Objects[i].Weight < 0{
			loadedSrcParam.Objects[i].Weight = 0
		}
	}

	return true
}

func list_load_xml(rawXML string) obs_config {
	loaded_xml := obs_config{}
	err_obs := xml.Unmarshal([]byte(rawXML), &loaded_xml)

	if err_obs != nil {
		fmt.Println("INFO: ", err_obs)
		u_exit("Fatal Error while loading configurations (observation).")
	}

	return loaded_xml
}

func list_export(obsObj obs, objects []src_obj, filename string) {
	var xmlStruct obs_config
	xmlStruct.Observation = obsObj
	xmlStruct.Sources = src{objects}

	output, _ := xml.MarshalIndent(xmlStruct, "  ", "    ")

	if filename == "" {
		os.Stdout.Write([]byte(xml.Header))
		os.Stdout.Write(output)
	} else {
		err := ioutil.WriteFile(filename, output, 0666)
		if err != nil {
			fmt.Println("[FAILED] Unable to export at the directort.")
		}
	}

	//test_export_as_sched(obsObj, objects)
}

func test_export_as_sched(obsObj obs, objects []src_obj) {
	for i := 0; i < len(objects); i++ {
		fmt.Println("source = "+objects[i].Identifier+"		dur = ", (objects[i].Duration), "	gap = ", (objects[i].Schedule.Gap), " setup = 'pfb20cm2'	/")
	}
}