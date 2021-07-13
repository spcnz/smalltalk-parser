import os
from fnmatch import fnmatch
from textx import metamodel_from_file
from model import Document, Workspace
from util import calculate_time
from multiprocessing import *

@calculate_time
def parse_all_parallel(workspace):
    with Pool() as pool:
        pool.map(parse_doc, list(workspace.documents.values()))


def parse_doc(doc):
    meta_model = metamodel_from_file("grammar/pharo.tx")
    doc.parse_model(meta_model)
    pass

def load_workspace(root, meta_model):
    workspace = Workspace(root, meta_model)
    pattern = "*.st"
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                file_name = os.path.join(path, name)
                doc = Document(file_name)
                workspace.add_document(doc)


    workspace.parse_all()
    # parse_all_parallel(workspace)

    return workspace

def start():

    root = 'examples\\'
    meta_model = metamodel_from_file("grammar/pharo.tx")
    workspace = load_workspace(root, meta_model)

if __name__ == '__main__':
    start()
