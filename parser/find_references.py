from textx.model import get_location, get_children
from util import parse_location, calculate_time

@calculate_time
def find_all_references(doc_uri, workspace, position):
    entity = find_entity(workspace.documents[doc_uri], position)
    print("FINDING MESSAGE : ", entity)
    result = []
    for doc in workspace.documents.values():
        reference_list = find_reference_in_doc(doc, entity)
        if reference_list:
            result += reference_list

    return result

def find_reference_in_doc(doc, entity):
    result = []
    a = 1
    if doc.is_valid_model:
        messages = get_children(check_type, doc.model)
        for msg in messages:
            reference_list = find_reference_in_msg(msg, entity)
            if reference_list:
                result += reference_list

    return result

def find_entity(doc, position):
    messages = get_children(check_type, doc.model)
    for msg in messages:

        if type(msg).__name__ == "KeywordMessage":
            for keyword in msg.keyword:
                location = get_location(keyword)
                if location['line'] == position.line and location['col'] == position.character:
                    return keyword.key

        else:
            location = get_location(msg)
            if location['line'] == position.line and location['col'] == position.character:
                return msg.selector

def check_type(el):
    return type(el).__name__ == "UnaryMessage" or type(el).__name__ == "BinaryMessage" or type(el).__name__ == "KeywordMessage"

def find_reference_in_msg(msg, entity):
    if type(msg).__name__ == "UnaryMessage":
        return check_unary_msg(msg, entity)
    elif type(msg).__name__ == "BinaryMessage":
        return check_binary_msg(msg, entity)
    elif type(msg).__name__ == "KeywordMessage":
        return check_keyword_msg(msg, entity)

#UNARY
def check_unary_msg(msg, entity):
    if not msg:
        return
    if entity == msg.selector:
        tx_location = get_location(msg)
        return [parse_location(tx_location, entity)]

# BINARY
def check_binary_msg(msg, entity):
    if not msg:
        return
    if entity == msg.selector:
        tx_location = get_location(msg)
        return [parse_location(tx_location, entity)]

# KEYWORD
def check_keyword_msg(msg, entity):
    if not msg:
        return
    result = []
    for keyword in msg.keyword:
        if entity == keyword.key:
            tx_location = get_location(keyword)

            result.append(parse_location(tx_location, entity))

    return result