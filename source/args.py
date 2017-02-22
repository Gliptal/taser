import argparse
import sys

import yaml

import log


RANGE = None
TARGET = None
FILE = None
LEEWAY = None
BASE = None
ROLL = None
TRACK = None
PICKLE = None
ABORT = None
FLOOR = None

def parse():
    global RANGE
    global TARGET
    global FILE

    parser = argparse.ArgumentParser(description="generate .xml files to visually render SLED attack profiles in the Tacview 3D environment")
    parser.add_argument("range", type=str, help="the range containing the attacked target")
    parser.add_argument("target", type=str, help="the attacked target")
    parser.add_argument("-o", "--out", type=str, help="specify a name for the generated .xml file", metavar="file", default="sled")
    parser.add_argument("-l", "--leeway", type=_positive_int, help="available leeway for all altitude values", metavar="ft", default=200)
    required_options = parser.add_argument_group("required SLED options")
    required_options.add_argument("-b", "--base", type=_positive_int, help="base distance (in nautical miles)", metavar="nm", required=True)
    required_options.add_argument("-r", "--roll", type=_positive_float, help="roll-in altitude (in feet)", metavar="ft", required=True)
    required_options.add_argument("-t", "--track", type=_positive_float, help="track altitude (in feet)", metavar="ft", required=True)
    required_options.add_argument("-p", "--pickle", type=_positive_float, help="release altitude (in feet)", metavar="ft", required=True)
    required_options.add_argument("-a", "--abort", type=_positive_float, help="abort altitude (in feet)", metavar="ft", required=True)
    required_options.add_argument("-f", "--floor", type=_positive_float, help="minimum altitude (in feet)", metavar="ft", required=True)

    args = parser.parse_args()

    RANGE = args.range
    TARGET = args.target
    FILE = args.out
    LEEWAY = args.leeway
    BASE = args.base
    ROLL = args.roll
    TRACK = args.track
    PICKLE = args.pickle
    ABORT = args.abort
    FLOOR = args.floor

def check_range():
    ranges = _load_ranges_data()

    found = False
    for item in ranges:
        if RANGE == item["name"]:
            found = True
            break

    if not found:
        log.fail("no such range "+RANGE)
        sys.exit()

def check_target():
    ranges = _load_ranges_data()

    for item in ranges:
        if RANGE == item["name"]:
            targets = item["targets"]
            break

    found = False
    for item in targets:
        if TARGET == item["name"]:
            found = True
            break

    if not found:
        log.fail("no such target "+TARGET+" in range "+RANGE)
        sys.exit()

def _positive_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")
    return number

def _positive_float(value):
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")
    return number

def _load_ranges_data():
    try:
        ranges_file = open("data/ranges.yaml")
        ranges_data = yaml.safe_load(ranges_file)
    except IOError:
        log.fail("missing data file")
        sys.exit()
    else:
        return ranges_data
