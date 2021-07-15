import itertools
import os
from fnmatch import fnmatch
from textx import metamodel_from_file
from lsp_model import Position
from model import Document, Workspace
from util import calculate_time
from multiprocessing import *
from multiprocessing.dummy import Pool as ThreadPool
from find_references import find_all_references

@calculate_time
def parse_all_parallel(workspace, meta_model):

    pool = ThreadPool(8)
    pool.starmap(parse_doc, zip(itertools.repeat(meta_model), list(workspace.documents.values())))

    # with Pool() as pool:
    #     pool.map(parse_doc, list(workspace.documents.values()))

def parse_doc(meta_model, doc):
        # meta_model = metamodel_from_file("grammar/pharo.tx")
    doc.parse_model(meta_model)

def load_workspace(root, meta_model):
    workspace = Workspace(root, meta_model)
    pattern = "*.st"
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                file_name = os.path.join(path, name)
                doc = Document(file_name)
                workspace.add_document(doc)


    # workspace.parse_all()
    parse_all_parallel(workspace, meta_model)

    return workspace

def start():
    print(cpu_count())
    root = 'examples\\'
    meta_model = metamodel_from_file("grammar/pharo.tx")
    workspace = load_workspace(root, meta_model)
    print("===============================")
    #
    # documentUri = "examples\\complex\\cascade.st"
    #
    # #hocu da nadjem poruku +
    # # documentUri = "examples\\messages\\keyword_msg.st"
    # # position = Position(line=3, character=15)
    #
    #FACTORIAL
    position = Position(line=10, character=5)
    documentUri = "examples\\messages\\unary_msg.st"

    result = find_all_references(documentUri, workspace, position)
    for loc in result:
        print(loc)
        print()


if __name__ == '__main__':
    start()
