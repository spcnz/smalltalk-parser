import traceback
from lsp_model import *
from st_parser import create_parser, parse_doc
import socketserver
from enum import Enum
from find_references import  find_all_references
from util import _content_length

workspace = None
meta_model = None

class MethodName(Enum):
        FIND_REFERENCES = "textDocument/references"
        CHANGED_DOCUMENT = "textDocument/didChange"
        INITIALIZED = "initialized"

        @classmethod
        def list(cls):
            return list(map(lambda c: c.value, cls))

class TCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle_method(self, request:RPCRequest):
        if request.method not in MethodName.list():
            raise Exception("Method not allowed")
        params = request.params
        if request.method == MethodName.INITIALIZED.value:
            global workspace
            global meta_model
            workspace, meta_model = create_parser(params['uri'])

        elif request.method == MethodName.FIND_REFERENCES.value:
            position = Position(params['position']['line'], params['position']['character'])
            documentUri = params['textDocument']['uri']
            result = find_all_references(documentUri, workspace, position)

            return result
        elif request.method == MethodName.CHANGED_DOCUMENT.value:
            documentUri = params['textDocument']['uri']
            parse_doc(meta_model, workspace.documents[documentUri])
        else:
            print("Error. Method not found.")


    def _read_message(self):
        line = self.rfile.readline()
        if not line:
            raise EOFError()
        content_length = _content_length(line)
        while line and line.strip():
            line = self.rfile.readline()
        if not line:
            raise EOFError()
        # Grab the body
        return self.rfile.read(content_length)

    def handle(self):
        self.data = self._read_message()
        print("{} wrote:".format(self.client_address[0]))
        json_data = json.loads(self.data.decode('utf-8'))
        request = RPCRequest(json_data) if 'id' in json_data.keys() else RPCNotification(json_data)
        try:
            response = self.handle_method(request)
            if isinstance(request, RPCNotification):
                return
            if (request.method == MethodName.FIND_REFERENCES.value):
                responses = [ location.toJSON() for location in response]
                self.request.sendall(bytes(json.dumps(responses), encoding="utf-8"))
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            print(err)
            error = RPCError(str(err))
            response = RPCResponse(None, error, request.id if hasattr(request, 'id') else None)
            print("Error sending : ", response.toJSON())

            self.request.sendall(bytes(response.toJSON(), encoding="utf-8"))


if __name__ == '__main__':
    HOST, PORT = "localhost", 9999
    print("Connection opened...")
    with socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler) as server:
        server.serve_forever()