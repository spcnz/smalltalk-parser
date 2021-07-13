from textx import metamodel_from_file, TextXSyntaxError
from textx.export import model_export
from os import listdir
from os.path import isfile, join
from subprocess import check_call



def print_stm(stm):
    if (type(stm).__name__ == "AssignmentExpression"):
        print("AssignmentExpression ", stm.var, ":=", stm.value)
    elif (type(stm).__name__ == "UnaryMessage"):
        print("UnaryMessage Poruka : ", stm.selector, " se salje objektu : ", stm.receiver)
    else:
        print(stm)


def find_unary_msg(model):
    pass


def start():
    file_names = [f for f in listdir("examples") if isfile(join("examples", f))]
    failed_num = 0


    meta_model = metamodel_from_file("grammar/pharo.tx")
    for file_name in file_names:
        try:
            model = meta_model.model_from_file("examples/" + file_name)

            find_unary_msg(model)
            dot_file_name = 'dot/' + file_name.replace(".st", "") +'.dot'
            model_export(model, dot_file_name)
            check_call(['dot','-Tpng',dot_file_name,'-o','images/' + file_name.replace(".st", "") + '.png'])

            #
            # print("========= SUCCESSFULLY PARSED ========")
            # print("FILE NAME : ", file_name)
            # print()

        except TextXSyntaxError as err:
            print ("========= TEST FAILED ========")
            print ("FILE NAME : ", file_name)
            print (err)
            print()
            failed_num += 1


    print()
    print("TEST FAILED : ", failed_num)
    print("TEST PASSED : ", len(file_names) - failed_num)


if __name__ == '__main__':
    start()
