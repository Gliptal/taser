import sys

from colorclass import Windows as colorize

import args
import log


colorize.enable()

args.parse()
args.check_range()
args.check_target()
