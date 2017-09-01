import lang.en as lang
import lang.prog as prog

import argparse
import types
import utils


MAIN   = None
WIRE   = None
SLED   = None
TARGET = None


def parse():
    global MAIN
    global WIRE
    global SLED
    global TARGET

    parser = argparse.ArgumentParser(description=lang.docs.MAIN, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=48))
    parser.add_argument("-v", "--version", action="version", version=prog.VERSION)
    parser.add_argument("-d", "--debug", action="store_true", help=lang.docs.FLAG_D)
    parser.add_argument("-f", "--filename", type=str, default="sled", help=lang.docs.FLAG_F, metavar=":str")
    parser.add_argument("-c", "--declutter", action="store_true", help=lang.docs.FLAG_C)

    optional_options = parser.add_argument_group(title=lang.docs.OPTIONAL)
    optional_options.add_argument("-ah", "--attackhdg", type=_heading,      default=None, help=lang.docs.FLAG_AH, metavar=":°")
    optional_options.add_argument("-lh", "--leewayhdg", type=_angle,        default=10,   help=lang.docs.FLAG_LH, metavar=":°")
    optional_options.add_argument("-la", "--leewayalt", type=_positive_int, default=200,  help=lang.docs.FLAG_LA, metavar=":ft")

    required_options = parser.add_argument_group(title=lang.docs.REQUIRED)
    required_options.add_argument("-ad", "--aimdist",    required=True, type=_positive_int, help=lang.docs.FLAG_AD, metavar=":ft")
    required_options.add_argument("-bd", "--basedist",   required=True, type=_positive_int, help=lang.docs.FLAG_BD, metavar=":ft")
    required_options.add_argument("-ba", "--basealt",    required=True, type=_positive_int, help=lang.docs.FLAG_BA, metavar=":ft")
    required_options.add_argument("-ta", "--trackalt",   required=True, type=_positive_int, help=lang.docs.FLAG_TA, metavar=":ft")
    required_options.add_argument("-ra", "--releasealt", required=True, type=_positive_int, help=lang.docs.FLAG_RA, metavar=":ft")
    required_options.add_argument("-aa", "--abortalt",   required=True, type=_positive_int, help=lang.docs.FLAG_AA, metavar=":ft")
    required_options.add_argument("-ma", "--minalt",     required=True, type=_positive_int, help=lang.docs.FLAG_MA, metavar=":ft")

    subparsers = parser.add_subparsers(title=lang.docs.MODE, dest="mode")
    parser_range = subparsers.add_parser("range", help=lang.docs.MODE_RANGE)
    parser_coords = subparsers.add_parser("coords", help=lang.docs.MODE_COORDS)

    parser_range.add_argument("code",       type=str,           help=lang.docs.MODE_RANGE_CODE)
    parser_range.add_argument("target",     type=str,           help=lang.docs.MODE_RANGE_TARGET)
    parser_coords.add_argument("latitude",  type=str,           help=lang.docs.MODE_COORDS_LAT)
    parser_coords.add_argument("longitude", type=str,           help=lang.docs.MODE_COORDS_LON)
    parser_coords.add_argument("altitude",  type=_positive_int, help=lang.docs.MODE_COORDS_ALT)

    args = parser.parse_args()

    MAIN = types.SimpleNamespace(MODE=args.mode, DEBUG=args.debug, FILENAME=args.filename, DECLUTTER=args.declutter)
    WIRE = types.SimpleNamespace(ATTACK_HDG=args.attackhdg, LEEWAY_HDG=args.leewayhdg, LEEWAY_ALT=args.leewayalt)
    SLED = types.SimpleNamespace(AIM_DIST=args.aimdist, BASE_DIST=args.basedist, BASE_ALT=args.basealt, TRACK_ALT=args.trackalt, RELEASE_ALT=args.releasealt, ABORT_ALT=args.abortalt, MIN_ALT=args.minalt)
    if MAIN.MODE == "range":
        TARGET = types.SimpleNamespace(RANGE=args.code, TARGET=args.target)
    elif MAIN.MODE == "coords":
        TARGET = types.SimpleNamespace(COORD_LAT=args.latitude, COORD_LON=args.longitude, ALTITUDE=args.altitude)


def check_range():
    global TARGET

    ranges = utils.data.load("data/ranges.yaml")
    found = False
    for item in ranges:
        if TARGET.RANGE == item["code"]:
            TARGET.RANGE = item
            found = True
            break

    if not found:
        raise ValueError("range", TARGET.RANGE)


def check_target():
    global TARGET

    ranges = utils.data.load("data/ranges.yaml")

    found = False
    for item in TARGET.RANGE["targets"]:
        if TARGET.TARGET == item["name"]:
            TARGET.TARGET = item
            found = True
            break

    if not found:
        raise ValueError("target", TARGET.TARGET, TARGET.RANGE["code"])


def convert():
    global WIRE
    global SLED

    if WIRE.ATTACK_HDG is not None:
        WIRE.ATTACK_HDG = utils.calc.thdg_to_mhdg(WIRE.ATTACK_HDG)
    WIRE.LEEWAY_ALT  = utils.calc.ft_to_m(WIRE.LEEWAY_ALT)
    SLED.AIM_DIST    = utils.calc.ft_to_m(SLED.AIM_DIST)
    SLED.BASE_DIST   = utils.calc.ft_to_m(SLED.BASE_DIST)
    SLED.BASE_ALT    = utils.calc.ft_to_m(SLED.BASE_ALT)
    SLED.TRACK_ALT   = utils.calc.ft_to_m(SLED.TRACK_ALT)
    SLED.RELEASE_ALT = utils.calc.ft_to_m(SLED.RELEASE_ALT)
    SLED.ABORT_ALT   = utils.calc.ft_to_m(SLED.ABORT_ALT)
    SLED.MIN_ALT     = utils.calc.ft_to_m(SLED.MIN_ALT)


def _positive_int(value):
    number = int(value)
    if not number >= 0:
        raise argparse.ArgumentTypeError(lang.error.INVALID_INT)

    return number


def _heading(value):
    number = int(value)
    if not (number >= 0 and number <= 359):
        raise argparse.ArgumentTypeError(lang.error.INVALID_HEADING)

    return number


def _angle(value):
    number = int(value)
    if not (number >= 0 and number <= 30):
        raise argparse.ArgumentTypeError(lang.error.INVALID_ANGLE)

    return number
