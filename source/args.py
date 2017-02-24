import argparse

import calc
import data
import log


RANGE = None
TARGET = None
FILE = None
LEEWAY = None
ENTRY = None
DIRECTION = None
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
    global DIRECTION
    global BASE
    global ROLL
    global TRACK
    global PICKLE
    global ABORT
    global FLOOR

    parser = argparse.ArgumentParser(description="generate .xml files to visually render SLED attack profiles in the Tacview 3D environment version: 0.6.0-beta1")
    parser.add_argument("-v", "--version", action="version", version="0.6.0-beta1")

    parser.add_argument("range", type=str, help="the range containing the attacked target")
    parser.add_argument("target", type=str, help="the attacked target")

    optional_options = parser.add_argument_group("optional other parameters")
    optional_options.add_argument("-o", "--out", type=str, help="name of the generated .xml file: default \"sled\"", metavar="file", default="sled")
    optional_options.add_argument("-l", "--leeway", type=_positive_int, help="available +/- leeway for the SLED's roll-in, release, and track altitudes (in feet) [default: 200ft]", metavar="ft", default=200)
    optional_options.add_argument("-e", "--entry", type=_angle, help="available +/- leeway for the range's attack heading at the SLED's roll-in altitude (in degrees) [default: 10°]", metavar="°", default=10)
    optional_options.add_argument("-d", "--direction", type=_heading, help="required attack heading, overrides the range's default (in degrees)", metavar="°", default=None)

    required_options = parser.add_argument_group("required SLED parametes")
    required_options.add_argument("-b", "--base", type=_positive_int, help="base distance (in nautical miles)", metavar="nm", required=True)
    required_options.add_argument("-r", "--roll", type=_positive_float, help="roll-in altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-t", "--track", type=_positive_float, help="track altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-p", "--pickle", type=_positive_float, help="release altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-a", "--abort", type=_positive_float, help="abort altitude (in feet MSL)", metavar="ft", required=True)
    required_options.add_argument("-f", "--floor", type=_positive_float, help="minimum altitude (in feet MSL)", metavar="ft", required=True)

    args = parser.parse_args()

    RANGE = args.range
    TARGET = args.target
    FILE = args.out
    LEEWAY = args.leeway
    ENTRY = args.entry
    DIRECTION = args.direction
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
        log.fail("no such range \""+RANGE+"\"")
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
        log.fail("no such target \""+TARGET+"\" in range \""+RANGE["name"]+"\"")
        raise Exception

def convert():
    global LEEWAY
    global DIRECTION
    global BASE
    global ROLL
    global TRACK
    global PICKLE
    global ABORT
    global FLOOR

    LEEWAY = calc.ft_to_m(LEEWAY)
    if DIRECTION is not None:
        DIRECTION = calc.thdg_to_mhdg(DIRECTION)
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

def _heading(value):
    number = int(value)
    if number < 0 or number > 359:
        raise argparse.ArgumentTypeError("heading must be between 0° and 359°")

    return number

def _angle(value):
    number = int(value)
    if number < 0 or number > 45:
        raise argparse.ArgumentTypeError("entry leeway must be between 0° and 45°")

    return number
