package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"net"

	"github.com/mitchellh/mapstructure"
	"github.com/sourcegraph/go-lsp"
)

var server LanguageServer = LanguageServer{}

func NewRPCResponseObject(id int, result interface{}, jsonrpc string) *RPCResponse {

	return &RPCResponse{
		ID:      id,
		Result:  result,
		JSONRPC: jsonrpc,
	}
}

func handleNotification(not *RPCNotification) error {
	if not.Method == string(INITIALIZED) {
		return server.initialized(not)
	} else if not.Method == string(CHANGED_DOCUMENT) {
		return server.textDocumentDidChange(not)
	} else {
		return errors.New("METHOD NOT FOUND")
	}
}

func handleRequest(req *RPCRequest) (*RPCResponse, error) {
	if req.Method == string(INITIALIZE) {
		var params *lsp.InitializeParams = &lsp.InitializeParams{}
		mapstructure.Decode(req.Params, &params)
		var result = server.initialize(params)
		var responseBody = NewRPCResponseObject(req.ID, result, req.JSONRPC)

		return responseBody, nil
	} else if req.Method == string(FIND_REFERENCES) {
		var result = server.findReferences(req)
		var responseBody = NewRPCResponseObject(req.ID, result, req.JSONRPC)

		return responseBody, nil
	} else {
		return nil, errors.New("METHOD NOT FOUND")
	}
}

func handleMsg(msg []byte) (*RPCResponse, error) {
	var req *RPCRequest = &RPCRequest{}
	var not *RPCNotification = &RPCNotification{}
	var m = make(map[string]interface{})
	err := json.Unmarshal(msg, &m)
	if err != nil {
		fmt.Println("Error while decoding it to map : ", err.Error())
		return nil, err
	}
	//check if it's a request or notification message
	if _, ok := m["id"]; ok {
		mapstructure.Decode(m, &req)
		return handleRequest(req)
	} else {
		mapstructure.Decode(m, &not)
		return nil, handleNotification(not)
	}
}

func main() {
	fmt.Println("Start server...")
	ln, _ := net.Listen("tcp", "localhost:8013")
	conn, _ := ln.Accept()
	buff := make([]byte, 512)
	var headerFound bool = false
	var savedData []byte = nil
	var size int = 512
	var err error = nil
	var response *RPCResponse = nil
	for {
		fmt.Println("READING ....")
		n, _ := conn.Read(buff)
		if !headerFound {
			size, savedData, err = readHeader(buff, n)
			if err != nil {
				fmt.Println("Error while getting header : ", err.Error())
			} else {
				headerFound = true
				buff = make([]byte, size)
			}
		} else {
			//header is found read rest of msg
			var message []byte
			//if some data is read with header part append it to rest of message
			if savedData != nil {
				message = append(savedData, buff...)
			} else {
				message = buff
			}
			fmt.Println(string(message))
			fmt.Println()
			response, err = handleMsg(message)
			if err == nil {
				if response != nil {
					conn.Write(format(response))
				}
			} else {
				fmt.Println("Error : ", err.Error())
			}
			buff = make([]byte, 512)
			headerFound = false
		}
	}
}
