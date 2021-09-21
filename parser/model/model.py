from textx import TextXSyntaxError
import logging
from logdecorator import log_on_start, log_on_error
from util.util import *

logging.basicConfig(level=logging.DEBUG)

class Workspace(object):
    def __init__(self, root_uri, meta_model):
        self.__root_uri = root_uri
        self._docs = {}
        self.__meta_model = meta_model

    @property
    def meta_model(self):
        return self.__meta_model

    @property
    def root_uri(self):
        return self.__root_uri

    @property
    def documents(self):
        return self._docs

    def get_document(self, doc_uri):
        try:
            return self._docs[doc_uri]
        except KeyError:
            return None

    def add_document(self, document, content=None):
        self._docs[document.uri] = document

    @calculate_time
    def parse_all(self):
        for doc in self.documents.values():
            doc.parse_model(self.__meta_model)


class Document(object) :
    def __init__(self, uri, source=None):
        self.__uri = uri
        self.__source = source
        self.__errors = []
        self.__model = None

    @property
    def uri(self):
        return self.__uri

    @property
    def source(self):
        if self._source is None:
            with open(self.uri, 'r') as f:
                self.__source = f.read()
        return self.__source

    @property
    def model(self):
        return self.__model

    @write_errors
    @convert_to_png
    @log_on_start(logging.DEBUG, "Start parsing doc {self.uri:s}...")
    def parse_model(self, meta_model):
        try:
            model = meta_model.model_from_file(self.__uri)
            self.__model = model
        except TextXSyntaxError as err:
            logging.error("\nSyntax error in file : {0}\n".format(self.__uri), exc_info=False)
            self.__errors.append(err)

        return self.__errors, self.__uri, self.__model

    @property
    def is_valid_model(self):
        return len(list(self.__errors)) == 0

    @property
    def errors(self):
        return self.__errors

