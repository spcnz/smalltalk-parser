import os
import time
from subprocess import check_call

from textx.export import model_export

def write_errors(func):
    def wrapper(*args, **kwargs):
        errors, uri, model = func(*args, **kwargs)
        if (len(errors) == 0):
            return errors, uri, model
        file_name = os.path.basename(uri).replace(".st", "")
        file_name = "log/" + file_name + "_errors.txt"
        with open(file_name, "w", encoding="utf-8") as writer:
            for err in errors:
                writer.write(err.message)
        return errors, uri, model

    return wrapper

def convert_to_png(func):
    def wrapper(*args, **kwargs):
        errors, uri, model = func(*args, **kwargs)
        if (len(errors) == 0):
            file_name = os.path.basename(uri)
            dot_file_name = 'dot/' + file_name.replace(".st", "") +'.dot'
            model_export(model, dot_file_name)
            check_call(['dot','-Tpng',dot_file_name,'-o','images/' + file_name.replace(".st", "") + '.png'])
        return errors, uri, model

    return wrapper

def calculate_time(func):

    def wrapper(*args, **kwargs):
        begin = time.time()

        result = func(*args, **kwargs)
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)

        return result

    return wrapper