import itertools
import os
from fnmatch import fnmatch
from textx import metamodel_from_file
from model import Document, Workspace
from util import calculate_time
from multiprocessing import *
from multiprocessing.dummy import Pool as ThreadPool

@calculate_time
def parse_all_parallel(workspace, meta_model):
    pool = ThreadPool(8)
    pool.starmap(parse_doc, zip(itertools.repeat(meta_model), list(workspace.documents.values())))

    # with Pool() as pool:
    #     result = pool.map(parse_doc, list(workspace.documents.values()))

def parse_doc(meta_model, doc):
        # meta_model = metamodel_from_file("grammar/pharo.tx")
    doc.parse_model(meta_model)

    # return doc

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

def create_parser(root):
    meta_model = metamodel_from_file("grammar/pharo.tx")
    workspace = load_workspace(root, meta_model)

    return workspace, meta_model