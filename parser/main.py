import os
from fnmatch import fnmatch
from textx import metamodel_from_file
from model import Document, Workspace
from util import calculate_time
from pathos.multiprocessing import ProcessingPool as Pool
from find_references import find_all_references


@calculate_time
def parse_all_parallel(workspace):
    with Pool() as pool:
        pool.map(parse_doc, list(workspace.documents.values()))



    # p = Process(target=f, args=(q,))
    # manager = Manager()
    # return_dict = manager.dict()
    # jobs = []
    # for doc in workspace.documents.values():
    #     p =  Process(target=parse_doc, args=(doc,q))
    #     jobs.append(p)
    #     p.start()


    # with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
    #     executor.map(parse_doc, list(workspace.documents.values()))
    # num = 0
    # # for doc in workspace.documents.values():
    # #     # print('a odje', doc.model)
    # #     if (doc.model == None):
    # #         # print (doc.uri,  'OVO NIJE PARSIRAO ZASTO?')
    # #         num += 1
    #
    # print("Ukupno dokumenata : ", len(workspace.documents))
    # print("Neparsirano : ", num)

def parse_doc(doc):
    meta_model = metamodel_from_file("grammar/pharo.tx")
    doc.parse_model(meta_model)
    print('parsiran? ', doc.model != None)

    return doc


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


    documentUri = "examples\\messages\\unary_msg.st"

    #hocu da nadjem poruku factorial
    position = {
        'line': 10,
        'character': 5
    }

    result = find_all_references(documentUri, workspace, position)
    for loc in result:
        print(loc)
        print()


if __name__ == '__main__':
    start()
