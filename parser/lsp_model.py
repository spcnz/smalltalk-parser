import json

class Position(object):
    def __init__(self, line: int, character: int):
        self.__line = line
        self.__character = character

    @property
    def line(self):
        return self.__line

    @property
    def character(self):
        return self.__character

    def __str__(self):
        return " { line: " + str(self.__line) + ", character: " + str(self.__character) + " }"

    def toJSON(self):
        return {
            "line" : self.__line,
            "character" : self.__character
        }



class Range(object):
    def __init__(self, start: Position, end: Position):
        self.__start = start
        self.__end = end

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    def __str__(self):
        return " { start: " + str(self.__start) + " end: " + str(self.__end) + " }"

    def toJSON(self):
        return {
            "start" : self.__start.toJSON(),
            "end" : self.__end.toJSON()
        }

class Location(object):
    def __init__(self, uri: str, range: Range):
        self.__uri = uri
        self.__range = range


    @property
    def uri(self):
        return self.__uri

    @property
    def range(self):
        return self.__range

    def __str__(self):
        return " { uri:" + self.__uri + ", range: " + str(self.__range) + " }"

    def toJSON(self):
        return {
            "uri": self.__uri,
            "range": self.__range.toJSON()
        }


class RPCNotification(object):
    def __init__(self, dict):
        self.__JSONRPC = "2.0"
        self.__method = dict['method']
        self.__params = dict['params']
    @property
    def method(self):
        return self.__method

    @property
    def params(self):
        return self.__params


class RPCRequest(object):
    def __init__(self, dict):
        self.__JSONRPC = "2.0"
        self.__method = dict['method']
        self.__params = dict['params']
        self.__id = dict['id']
    @property
    def method(self):
        return self.__method

    @property
    def params(self):
        return self.__params

    @property
    def id(self):
        return self.__id


class RPCError(object):
    def __init__(self,  message: str, code: int = None, data=None):
        self.__code = code
        self.__message = message
        self.__data = data

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    def toJSON(self):
        return {
            "code" : self.__code,
            "message" : self.__message
        }


class RPCResponse(object):
    def __init__(self, result, error: RPCError, id):
        self.__JSONRPC = "2.0"
        self.__result = result
        self.__error = error
        self.__id = id
    @property
    def result(self):
        return self.__result

    @property
    def error(self):
        return self.__error

    @property
    def id(self):
        return self.__id

    def list_to_json(self):
        return [location.toJSON() for location in self.__result]

    def toJSON(self):
        result_json = self.list_to_json() if self.__result else None
        error_json = self.__error.toJSON() if self.error else None

        return json.dumps({
            "id" : self.__id,
            "error" : error_json,
            "result" : result_json,
            "jsonrpc": self.__JSONRPC,
        })
