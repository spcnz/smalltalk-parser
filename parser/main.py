import os
from fnmatch import fnmatch
from textx import metamodel_from_file
from model import Document, Workspace
from util import calculate_time


def find_unary_msg(model):
    pass

@calculate_time
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

    return workspace

def start():
    root = 'examples\\'
    meta_model = metamodel_from_file("grammar/pharo.tx")
    workspace = load_workspace(root, meta_model)

if __name__ == '__main__':
    start()
