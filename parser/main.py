import traceback
from lsp_model import *
from st_parser import create_parser
import socketserver
from enum import Enum
from find_references import  find_all_references


workspace = None

class MethodName(Enum):
        CREATE_PARSER = "createParser"
        FIND_REFERENCES = "findReferences"
        CHANGED_DOCUMENT = "changedDocument"

        @classmethod
        def list(cls):
            return list(map(lambda c: c.value, cls))


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle_method(self, request:RPCRequest):

        if request.method not in MethodName.list():
            raise Exception("Method not allowed")
        params = request.params[0]

        if request.method == MethodName.CREATE_PARSER.value:
            global workspace
            workspace = create_parser(params['uri'])

        elif request.method == MethodName.FIND_REFERENCES.value:
            position = Position(params['position']['line'], params['position']['character'])
            documentUri = params['textDocument']['uri']
            result = find_all_references(documentUri, workspace, position)

            return result

        elif request.method == MethodName.CHANGED_DOCUMENT.value:
            pass


    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        json_data = json.loads(self.data)
        request = RPCRequest(json_data) if 'id' in json_data.keys() else RPCNotification(json_data)

        try:
            response = self.handle_method(request)
            if isinstance(request, RPCNotification):
                return
            responses = { "locations" : [ location.toJSON() for location in response] }
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
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        server.serve_forever()
