package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strings"
)

func u_file_get_contents(filename string) (string, bool) {
	fileObj, error := ioutil.ReadFile(filename)

	if error == nil {
		return string(fileObj), false
	} else {
		return string(fileObj), true
	}
}

func u_file_put_contents(filename, text string) bool {
	error := ioutil.WriteFile(filename, []byte(text), 0666)

	if error == nil {
		return false
	} else {
		return true
	}
}

func u_file_get_file_annotated(filename string) string {
	fileObj, error := os.Open(filename)

	rawJson := "{}"
	if error == nil {
		rawJson = ""
		linesHandle := bufio.NewReader(fileObj)
		for {
			thisLineBytes, _, status := linesHandle.ReadLine()
			thisLine := string(thisLineBytes)

			if status == io.EOF {
				break
			}

			if strings.Contains(thisLine, "#") {
				// if !strings.HasPrefix(strings.Replace(thisLine, " ", "", -1), "#") {
				//     rawJson = strings.Join([]string{rawJson, thisLine}, "\n")
				// }
				thisLine = thisLine[0:strings.Index(thisLine, "#")]
			}

			rawJson = strings.Join([]string{rawJson, thisLine}, "\n")
		}
	} else {
		fmt.Println("File not found:", filename)
		return ""
	}

	defer fileObj.Close()
	return rawJson
}

func u_progress_bar(now int64, full int64) {
	//text0 := "████████████████████"
	//text1 := "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
	//length := int64(len(text0))

	//fmt.Printf(strings.Join([]string{text0[0 : length*(now/full)], text1[length*(now/full) : length]}, ""))

	return
}

func u_progress_bar_end(text string) {
	fmt.Printf(text)

	return
}
