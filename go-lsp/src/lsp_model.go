package main

import "encoding/json"

type MethodName string

type LSPService struct{}

const (
	StopCharacter = "\r\n\r\n"
)

const (
	CREATE_PARSER    MethodName = "createParser"
	FIND_REFERENCES  MethodName = "findReferences"
	CHANGED_DOCUMENT MethodName = "changedDocument"
)

type TextDocumentIdentifier struct {
	Uri string `json:"uri"`
}

type RPCRequest struct {
	JSONRPC string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
	ID      string      `json:"id"`
}

type RPCNotification struct {
	JSONRPC string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
}

type RPCResponse struct {
	JSONRPC string      `json:"jsonrpc"`
	Result  interface{} `json:"result,omitempty"`
	Error   *RPCError   `json:"error,omitempty"`
	ID      string      `json:"id"`
}

type RPCError struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

//REFERENCES
type Position struct {
	Line      json.Number `json:"line"`
	Character json.Number `json:"character"`
}

type Range struct {
	Start Position `json:"start"`
	End   Position `json:"end"`
}

type Location struct {
	Uri   string `json:"uri"`
	Range Range  `json:"range"`
}

type ReferenceParams struct {
	TextDocument TextDocumentIdentifier `json:"textDocument"`
	Position     Position               `json:"position"`
}

type ReferenceResponse struct {
	Locations []Location `json:"locations"`
}
