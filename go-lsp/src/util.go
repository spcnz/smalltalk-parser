package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/url"
	"strconv"
	"strings"
)

// getContentLength reads from header string size of content
// It returns the content length read from header
func getContentLength(header string) (int, error) {
	var length = strings.Split(header, ":")[1]
	size, err := strconv.Atoi(strings.TrimSpace(length))
	if err != nil {
		return 0, err
	} else {
		return size, nil
	}
}

// readHeader reads from byte buffer buff (which contains n bytes) and search for header part
// Header is separated from rest data with \r\n\r\n
// Buffer can sometimes include part of data after header
// It returns the content length read from header and (optionally) part of data after header part
func readHeader(buff []byte, n int) (int, []byte, error) {
	var str = string(buff[0:n])
	var arr = strings.SplitAfter(str, "\r\n\r\n")
	if len(arr) > 0 {
		header := arr[0]
		var size, err = getContentLength(header)
		if err != nil {
			fmt.Println("Error while getting size of string")
			return 0, nil, err
		} else {
			if len(strings.TrimSpace(arr[1])) == 0 {
				//"No additional data with header part"
				return size, nil, nil
			} else {
				var savedData = []byte(arr[1])
				//Content length for next message is now size - length of part that came with header
				return size - len(savedData), savedData, nil

			}
		}
	} else {
		//buffer doesn't contain header part (it should be separated with "\r\n\r\n")
		return 0, nil, errors.New("HEADER PART IS MISSING")
	}
}

// Format adds header part to response body
// It id used for sending RPCResponse, RPCRequest and RPCNotification objects over network
// It returns byte representation of response with header
func format(body interface{}) []byte {
	json, err := json.Marshal(body)
	fmt.Println("JSOOON ", string(json))
	if err != nil {
		fmt.Println("Error while marshaling to json : ", err.Error())
		return nil
	}
	return []byte(fmt.Sprintf("Content-Length: %d\r\nContent-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n%s", len(json), json))
}

// parseUri replace '/' with '\\' and removes 'file:' part from uri
// It returns rest of uri without root path
func parseUri(uri string) string {
	parsedURL, _ := url.PathUnescape(uri)
	arr := strings.Split(parsedURL, "/")
	parsedURL = strings.Join(arr[3:], "\\")

	return parsedURL
}
