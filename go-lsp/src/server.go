package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"

	"github.com/mitchellh/mapstructure"
	"github.com/sourcegraph/go-lsp"
)

type LanguageServer struct {
	rootPath     string
	initOptions  lsp.InitializeParams
	capabilities ServerCapabilities
}

//Python parser socket address
const (
	ip   = "127.0.0.1"
	port = 9999
)

// Initialize saves rootPath as param of language server
// It returns InitializeResult with definied server capabilities : findReferences capability
func (ls *LanguageServer) initialize(params *lsp.InitializeParams) *InitializeResult {
	ls.rootPath = (*params).RootPath
	fmt.Println("saved rootPath is : ", ls.rootPath)
	ls.initOptions = *params

	ls.capabilities = ServerCapabilities{TextDocumentSync: TextDocumentKind(1), ReferenceProvider: true}

	var result = InitializeResult{Capabilities: ls.capabilities}

	return &result
}

// Initialized sends initialized notification to python parser after which parser is created
func (ls *LanguageServer) initialized(not *RPCNotification) error {
	addr := strings.Join([]string{ip, strconv.Itoa(port)}, ":")
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		log.Fatalln(err)
		os.Exit(1)
	}
	defer conn.Close()
	not.Params = TextDocumentIdentifier{Uri: ls.rootPath}
	conn.Write(format(not))

	return nil
}

func (ls *LanguageServer) textDocumentDidChange(not *RPCNotification) error {
	//ovde ce inace slati promena stanaj python parseru eh tu suuu super
	addr := strings.Join([]string{ip, strconv.Itoa(port)}, ":")
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		log.Fatalln(err)
		os.Exit(1)
	}
	defer conn.Close()
	var params *DidChangeTextDocumentParams = &DidChangeTextDocumentParams{}
	mapstructure.Decode(not.Params, &params)
	params.TextDocument.Uri = parseUri(params.TextDocument.Uri)
	not.Params = params
	conn.Write(format(not))

	return nil
}

func (ls *LanguageServer) findReferences(req *RPCRequest) *[]Location {
	addr := strings.Join([]string{ip, strconv.Itoa(port)}, ":")
	conn, err := net.Dial("tcp", addr)

	if err != nil {
		log.Fatalln(err)
		os.Exit(1)
	}
	defer conn.Close()
	//SENDING DATA
	paramsMap := req.Params.(map[string]interface{})
	var params *ReferenceParams = &ReferenceParams{}
	mapstructure.Decode(paramsMap, &params)
	params.TextDocument.Uri = parseUri(params.TextDocument.Uri)
	params.Position.Character += 1
	params.Position.Line += 1
	req.Params = params
	conn.Write(format(req))

	// RECEIVING DATA
	var response *[]Location
	error_dec := json.NewDecoder(conn).Decode(&response)

	if error_dec != nil {
		log.Print("Error while converting response from bytes to json : ", error_dec.Error())
		return nil
	} else {
		for i := 0; i < len(*response); i++ {
			var loc = &(*response)[i]
			loc.Uri = "file:///" + loc.Uri
			loc.Range.Start.Line -= 1
			loc.Range.Start.Character -= 1
			loc.Range.End.Line -= 1
			loc.Range.End.Character -= 1
		}

		return response
	}
}
