from textx.model import get_location, get_children
from util import parse_location, calculate_time

global references

references = []

@calculate_time
def find_all_references(doc_uri, workspace, position):

    #ovde cu pronaci entitet nekako preko pozicije
    entity = "factorial"
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


#
# def find_reference(model, entity):
#     if not model:
#         return
#
#     for statement in model.statements:
#         if type(statement).__name__ == "ReturnStatement":
#             check_expression(statement.returnExp, entity)
#         else:
#             if (statement.exp):
#                 check_expression(statement.exp, entity)
#             for exp in statement.list:
#                 check_expression(exp, entity)


def check_expression(exp, entity):

    #if expression is literal continue
    if exp.literal:
        check_literal(exp.literal, entity)
    elif exp.assignment:
        check_expression(exp.assignment.value, entity)

    if type(exp.send).__name__ == "BinarySend":

        check_binary_send(exp.send, entity)
    elif type(exp.send).__name__ == "UnarySend":

        check_unary_send(exp.send, entity)
    elif type(exp.send).__name__ == "KeywordSend":

        check_keyword_send(exp.send, entity)
    elif type(exp.send).__name__ == "Cascade":
        print('hereee')
        check_cascade(exp.send, entity)



# UNARY
def check_unary_send(unary_send, entity):
    if not unary_send:
        return
    check_unary_tail(unary_send.selector, entity)

def check_unary_tail(tail, entity):
    if not tail:
        return
    check_unary_msg(tail.msg, entity)

    #recursion call
    check_unary_tail(tail.tail, entity)

def check_unary_msg(msg, entity):
    if entity == msg.unarySelector:
        tx_location = get_location(msg)
        references.append(parse_location(tx_location, entity))


# BINARY
def check_binary_send(binary_send, entity):
    if not binary_send:
        return
    if type(binary_send.receiver).__name__ == "UnarySend":
        check_unary_send(binary_send.receiver, entity)

    check_binary_tail(binary_send.tail, entity)

def check_binary_tail(tail, entity):
    if not tail:
        return
    check_binary_msg(tail.msg, entity)

    # recursion call
    check_unary_tail(tail.tail, entity)

def check_binary_msg(msg, entity):
    if entity == msg.selector:
        tx_location = get_location(msg)
        references.append(parse_location(tx_location, entity))
    if type(msg.arg).__name__ == "UnarySend":
        check_unary_send(msg.arg, entity)


# KEYWORD
def check_keyword_send(keyword_send, entity):
    if not keyword_send:
        return
    if type(keyword_send.receiver).__name__ == "UnarySend":
        check_unary_send(keyword_send.receiver, entity)

    check_keyword_msg(keyword_send.msg, entity)

def check_keyword_msg(msg, entity):
    if not msg:
        return
    for keyword in msg.keyword:
        if entity == keyword.key:
            tx_location = get_location(msg)
            references.append(parse_location(tx_location, entity))
        if type(keyword.arg).__name__ == "BinarySend":
            check_binary_send(keyword.arg, entity)

# CASCADE
def check_cascade(cascade, entity):
    if not cascade:
        return
    if type(cascade.receiver).__name__ == "KeywordSend":
        check_keyword_send(cascade.receiver, entity)
    elif type(cascade.receiver).__name__ == "BinarySend":
        check_binary_send(cascade.receiver, entity)
    elif type(cascade.receiver).__name__ == "UnarySend":
        check_unary_send(cascade.receiver, entity)

    for selector in cascade.selectors:
        if type(selector).__name__ == "KeywordMessage":
            check_keyword_msg(selector, entity)
        elif type(selector).__name__ == "BinaryMessage":
            check_binary_msg(selector, entity)
        elif type(selector).__name__ == "UnaryMessage":
            check_unary_msg(selector, entity)

#LITERAL
def check_literal(literal, entity):
    if type(literal).__name__ == "RuntimeLiteral":
        find_reference(literal.block.body, entity)

#RECEIVER
def check_receiver(receiver, entity):
    pass