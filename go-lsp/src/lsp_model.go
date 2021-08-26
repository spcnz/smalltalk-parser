package main

type MethodName string

type LSPService struct{}

const (
	StopCharacter = "\r\n\r\n"
)

const (
	FIND_REFERENCES  MethodName = "textDocument/references"
	CHANGED_DOCUMENT MethodName = "textDocument/didChange"
	INITIALIZE       MethodName = "initialize"
	INITIALIZED      MethodName = "initialized"
)

type TextDocumentKind int

const (
	NONE        TextDocumentKind = 0
	FULL        TextDocumentKind = 1
	INCREMENTAL TextDocumentKind = 2
)

type TextDocumentIdentifier struct {
	Uri string `json:"uri"`
}

type RPCRequest struct {
	JSONRPC string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
	ID      int         `json:"id"`
}

type RPCNotification struct {
	JSONRPC string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
}

type RPCResponse struct {
	JSONRPC string      `json:"jsonrpc"`
	Result  interface{} `json:"result,omitempty"`
	ID      int         `json:"id"`
}

type RPCError struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

//REFERENCES
type Position struct {
	Line      float64 `json:"line"`
	Character float64 `json:"character"`
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

type ContentChanges struct {
	Text string `json:"text"`
}

type DidChangeTextDocumentParams struct {
	TextDocument   TextDocumentIdentifier `json:"textDocument"`
	ContentChanges ContentChanges         `json:"contentChanges"`
	Version        int                    `json:"version"`
}

type InitializeResult struct {
	Capabilities ServerCapabilities `json:"capabilities,omitempty"`
}

type ServerCapabilities struct {
	TextDocumentSync  TextDocumentKind `json:"textDocumentSync"`
	ReferenceProvider bool             `json:"referencesProvider"`
}
