import argparse

import calc
import data
import log


RANGE = None
TARGET = None
FILE = None
LEEWAY = None
ENTRY = None
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
    global LEEWAY
    global ENTRY
    global BASE
    global ROLL
    global TRACK
    global PICKLE
    global ABORT
    global FLOOR

    parser = argparse.ArgumentParser(description="generate .xml files to visually render SLED attack profiles in the Tacview 3D environment")
    parser.add_argument("range", type=str, help="the range containing the attacked target")
    parser.add_argument("target", type=str, help="the attacked target")
    parser.add_argument("-o", "--out", type=str, help="name of the generated .xml file", metavar="file", default="sled")
    parser.add_argument("-l", "--leeway", type=_positive_int, help="available +/- leeway for roll-in, track, and release altitudes (in feet): default 200ft", metavar="ft", default=200)
    parser.add_argument("-e", "--entry", type=_positive_int, help="available +/- leeway for the attack heading at roll-in (in degrees): defaulr 3°", metavar="°", default=3)
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
    ENTRY = args.entry
    BASE = args.base
    ROLL = args.roll
    TRACK = args.track
    PICKLE = args.pickle
    ABORT = args.abort
    FLOOR = args.floor

def check_range():
    global RANGE

    ranges = data.load("data/ranges.yaml")

    found = False
    for item in ranges:
        if RANGE == item["name"]:
            RANGE = item
            found = True
            break

    if not found:
        log.fail("no such range "+RANGE)
        raise Exception

def check_target():
    global TARGET

    ranges = data.load("data/ranges.yaml")

    found = False
    for item in RANGE["targets"]:
        if TARGET == item["name"]:
            TARGET = item
            found = True
            break

    if not found:
        log.fail("no such target "+TARGET+" in range "+RANGE["name"])
        raise Exception

def convert():
    global LEEWAY
    global BASE
    global ROLL
    global TRACK
    global PICKLE
    global ABORT
    global FLOOR

    LEEWAY = calc.ft_to_m(LEEWAY)
    BASE = calc.ft_to_m(BASE)
    ROLL = calc.ft_to_m(ROLL)
    TRACK = calc.ft_to_m(TRACK)
    PICKLE = calc.ft_to_m(PICKLE)
    ABORT = calc.ft_to_m(ABORT)
    FLOOR = calc.ft_to_m(FLOOR)

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
