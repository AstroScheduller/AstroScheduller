/*
 * @Author: your name
 * @Date: 2022-01-06 00:53:26
 * @LastEditTime: 2022-03-17 20:57:19
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /AstroSchedullerPy/Users/wenky/Library/CloudStorage/OneDrive-Franklin&MarshallCollege/Astro/AstroSchedullerGo/list.go
 */
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
		if loadedSrcParam.Objects[i].Important != 1 {
			loadedSrcParam.Objects[i].Important = 0
		}

		if loadedSrcParam.Objects[i].Weight > 1 || loadedSrcParam.Objects[i].Weight < 0 {
			loadedSrcParam.Objects[i].Weight = 0
		}
	}

	if loadedObsParam.Escape.Sun != 0 {
		loadedObsParam.Escape.Sun = loadedObsParam.Escape.Sun + 3 // For the reason that estimated AltAz overall has an 3 degree error.
	}

	return true
}

func list_load_xml(rawXML string) obs_config {
	loaded_xml := obs_config{}
	err_obs := xml.Unmarshal([]byte(rawXML), &loaded_xml)

	if err_obs != nil {
		fmt.Println("Error:", err_obs)
	}

	return loaded_xml
}

func list_construct_xml(obsObj obs, objects []src_obj) []byte {
	var xmlStruct obs_config
	xmlStruct.Observation = obsObj
	xmlStruct.Sources = src{objects}

	output, _ := xml.MarshalIndent(xmlStruct, "  ", "    ")

	return output
}

func list_export(obsObj obs, objects []src_obj, filename string) {
	output := list_construct_xml(obsObj, objects)

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
