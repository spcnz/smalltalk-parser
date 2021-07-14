from textx.model import get_location, get_children
from util import parse_location, calculate_time

global references

references = []

@calculate_time
def find_all_references(doc_uri, workspace, position):

    #ovde cu pronaci entitet nekako preko pozicije
    entity = "show:"
    for doc_uri, doc in workspace.documents.items():
        global expNum
        expNum = 0
        if doc.is_valid_model:
            messages = get_children(check_type, doc.model)
            for msg in messages:
                find_reference(msg, entity)
            # find_reference(doc.model, "factorial")

    return references

def check_type(el):
    return type(el).__name__ == "UnaryMessage" or type(el).__name__ == "BinaryMessage" or type(el).__name__ == "KeywordMessage"

def find_reference(msg, entity):
    if type(msg).__name__ == "UnaryMessage":
        check_unary_msg(msg, entity)
    elif type(msg).__name__ == "BinaryMessage":
        check_binary_msg(msg, entity)
    elif type(msg).__name__ == "KeywordMessage":
        check_keyword_msg(msg, entity)

#UNARY
def check_unary_msg(msg, entity):
    if not msg:
        return
    if entity == msg.unarySelector:
        tx_location = get_location(msg)
        references.append(parse_location(tx_location, entity))


# BINARY
def check_binary_msg(msg, entity):
    if not msg:
        return
    if entity == msg.selector:
        tx_location = get_location(msg)
        references.append(parse_location(tx_location, entity))

# KEYWORD
def check_keyword_msg(msg, entity):
    if not msg:
        return
    for keyword in msg.keyword:
        if entity == keyword.key:
            tx_location = get_location(msg)
            references.append(parse_location(tx_location, entity))