import sys

from colorclass import Windows as colorize

import args
import log
import tacview


colorize.enable()

try:
    args.parse()
    args.check_range()
    args.check_target()
    args.convert()
except SystemExit:
    raise
except Exception as ex:
    if args.DEBUG:
        log.fail("an error occured: "+str(ex))
    else:
        log.fail("an error occured")
    sys.exit()

log.tentative("generating "+args.FILE+".xml")
try:
    tacview.generate()
    log.success(args.FILE+".xml generated")
except Exception as ex:
    if args.DEBUG:
        log.fail("an error occured: "+str(ex))
    else:
        log.fail("an error occured")
    sys.exit()
