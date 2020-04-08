import os


def convert_ui(path_in=".", path_out="."):
    for r, d, f in os.walk(path_in):
        for file in f:
            if '.ui' in file:
                os.system("pyuic5 {0}/{1} > {3}/{2}".format(path_in, file, file.replace('.ui', '.py'), path_out))


def convert_resources(path_in=".", path_out="."):
    for r, d, f in os.walk(path_in):
        for file in f:
            if '.qrc' in file:
                os.system("pyrcc5 {0}/{1} > {3}/{2}".format(path_in, file, file.replace('.qrc', '_rc.py'), path_out))


if __name__ == "__main__":
    convert_ui("./ui", "./ui/py")
    convert_resources("./resources", "./resources/py")
