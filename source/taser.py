import args
import colorclass
import lang.en as lang
import sys
import tacview
import utils


colorclass.Windows.enable()

try:
    args.parse()
    utils.log.tentative(lang.execution.VALIDATING)
    if args.MAIN.MODE == "range":
        args.check_range()
        args.check_target()
    args.convert()
    utils.log.success(lang.execution.VALIDATED)
except SystemExit:
    raise
except IOError:
    utils.log.fail(lang.error.MISSING_FILE)
    sys.exit()
except ValueError as ex:
    if ex.args[0] == "range":
        utils.log.fail(lang.error.INVALID_RANGE % (ex.args[1]))
    elif ex.args[0] == "target":
        utils.log.fail(lang.error.INVALID_TARGET % (ex.args[1], ex.args[2]))
    sys.exit()
except Exception as ex:
    if args.MAIN.DEBUG:
        utils.log.fail(lang.error.DEBUG % (str(ex)))
    else:
        utils.log.fail(lang.error.GENERIC)
    sys.exit()

utils.log.tentative(lang.execution.GENERATING % (args.MAIN.FILENAME))
try:
    tacview.generate()
    utils.log.success(lang.execution.GENERATED % (args.MAIN.FILENAME))
except Exception as ex:
    if args.MAIN.DEBUG:
        utils.log.fail(lang.error.DEBUG % (str(ex)))
    else:
        utils.log.fail(lang.error.GENERIC)
    sys.exit()
