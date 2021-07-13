from textx import metamodel_from_file, TextXSyntaxError
from textx.export import model_export


def print_stm(stm):
    if (type(stm).__name__ == "AssignmentExpression"):
        print("AssignmentExpression ", stm.var, ":=", stm.value)
    elif (type(stm).__name__ == "UnaryMessage"):
        print("UnaryMessage Poruka : ", stm.selector, " se salje objektu : ", stm.receiver)
    else:
        print(stm)


def start():
    file_names = ['comment_only.st', 'simple_without_msg.st']
    meta_model = metamodel_from_file("grammar/pharo.tx")
    for file_name in file_names:
        try:
            model = meta_model.model_from_file("examples/" + file_name)
            if (hasattr(model, "statements")):
                for stm in model.statements:
                    if (type(stm).__name__ == "AssignmentExpression") :
                        print ("AssignmentExpression ", stm.var , ":=", stm.value)
                    elif (type(stm).__name__ == "UnaryMessage") :
                        print ("UnaryMessage Poruka : ", stm.selector ," se salje objektu : " )
                        print_stm(stm.receiver)
                    elif (type(stm).__name__ == "BinaryMessage"):
                        print("BinaryMessage Poruka : ", stm.selector, " se salje objektu : ")
                        print_stm(stm.receiver)
                        print(" sa argumentom : ", stm.arg)
                    else:
                        print(type(stm), stm)
                    print("===========")
            model_export(model, file_name +'.dot')
            print("========= SUCCESSFULLY PARSED ========")
            print("FILE NAME : ", file_name)
            print()

        except TextXSyntaxError as err:
            print ("========= TEST FAILED ========")
            print ("FILE NAME : ", file_name)
            print (err)
            print()


if __name__ == '__main__':
    start()
