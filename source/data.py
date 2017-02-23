import yaml

import log


def load(path):
    try:
        file = open(path)
        data = yaml.safe_load(file)
        file.close()
    except IOError:
        log.fail("missing data file")
    else:
        return data
