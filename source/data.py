import os
import sys

import yaml

import log


def load(path):
    try:
        file = open(resource_path(path))
        data = yaml.safe_load(file)
        file.close()
    except IOError:
        log.fail("missing data file")
    else:
        return data

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
