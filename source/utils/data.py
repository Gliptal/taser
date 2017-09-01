import os
import sys
import yaml
import yamlordereddictloader


def load(path):
    try:
        file = open(_resource_path(path))
        data = yaml.load(file, Loader=yamlordereddictloader.Loader)
        file.close()
    except IOError:
        raise
    else:
        return data


def save(path, data):
    output_file = open(path+".xml", "w+")
    output_file.write(data)
    output_file.close()


def _resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
