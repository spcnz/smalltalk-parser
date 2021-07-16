package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"

	enc "encoding/json"

	"github.com/gorilla/mux"
	"github.com/gorilla/rpc"
	"github.com/gorilla/rpc/json"
	uuid "github.com/nu7hatch/gouuid"
)

var ID uint

//DOCUMENT DID OPEN
func (t *LSPService) DidOpen(r *http.Request, args *TextDocumentIdentifier, result *RPCResponse) error {

	var (
		ip   = "127.0.0.1"
		port = 9999
	)
	createParserSocket(ip, port, args)
	return nil
}

type Response struct {
	Result string
}

//FIND REFERENCES
func (t *LSPService) References(r *http.Request, args *ReferenceParams, result *interface{}) error {

	var (
		ip   = "127.0.0.1"
		port = 9999
	)
	response := findReferencesSocket(ip, port, args)
	*result = response

	return nil
}

func createParserSocket(ip string, port int, params *TextDocumentIdentifier) {
	addr := strings.Join([]string{ip, strconv.Itoa(port)}, ":")
	conn, err := net.Dial("tcp", addr)

	if err != nil {
		log.Fatalln(err)
		os.Exit(1)
	}

	defer conn.Close()

	notification := NewRPCNotificationObject(CREATE_PARSER, params)

	//SENDING DATA
	error_enc := enc.NewEncoder(conn).Encode(notification)
	log.Printf("NOTIFICATION ")
	log.Printf("Send method: %s", notification.Method)
	log.Printf("Send params: %s", notification.Params)

	if error_enc != nil {
		log.Print("Error while converting notification to json : ", error_enc)
	}
}

func findReferencesSocket(ip string, port int, params *ReferenceParams) interface{} {
	addr := strings.Join([]string{ip, strconv.Itoa(port)}, ":")
	conn, err := net.Dial("tcp", addr)

	if err != nil {
		log.Fatalln(err)
		os.Exit(1)
	}

	defer conn.Close()

	request := NewRPCRequestObject(FIND_REFERENCES, params)
	fmt.Print("\nID : \n", request.ID)

	//SENDING DATA
	error_enc := enc.NewEncoder(conn).Encode(request)
	log.Printf("REQUEST ")
	log.Printf("Send method: %s", request.Method)
	log.Printf("Send params: %s", request.Params)

	if error_enc != nil {
		log.Print("Error while converting request to json : ", error_enc)
	}

	//RECEIVING DATA
	var response *ReferenceResponse

	error_dec := enc.NewDecoder(conn).Decode(&response)

	if error_dec != nil {
		log.Print("Error while converting response from bytes to json : ", error_dec)

		return response
	} else {
		return response.Locations
	}
}

func NewRPCNotificationObject(method MethodName, params ...interface{}) *RPCNotification {
	rpcNotification := RPCNotification{
		JSONRPC: "2.0",
		Method:  string(method),
		Params:  params,
	}

	if len(params) == 0 {
		rpcNotification.Params = nil
	}

	return &rpcNotification
}

func NewRPCRequestObject(method MethodName, params ...interface{}) *RPCRequest {
	u, err := uuid.NewV4()
	if err != nil {
		fmt.Print("Error while generating unique ID.")
	}
	rpcRequest := RPCRequest{
		ID:      u.String(),
		JSONRPC: "2.0",
		Method:  string(method),
		Params:  params,
	}

	return &rpcRequest
}

func main() {

	rpcServer := rpc.NewServer()

	rpcServer.RegisterCodec(json.NewCodec(), "application/json")
	rpcServer.RegisterCodec(json.NewCodec(), "application/json;charset=UTF-8")

	service := new(LSPService)

	rpcServer.RegisterService(service, "textDocument")

	router := mux.NewRouter()
	router.Handle("/", rpcServer)
	http.ListenAndServe(":8000", router)

}
