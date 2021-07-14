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