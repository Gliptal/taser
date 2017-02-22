import sys

import yaml

import log


def load_data(path):
    try:
        file = open(path)
        data = yaml.safe_load(file)
    except IOError:
        log.fail("missing data file")
        sys.exit()
    else:
        return data
