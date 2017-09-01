import colorclass


POSITIVE  = "+"
NEGATIVE  = "-"
NEUTRAL   = "?"
SEPARATOR = "    "


def success(string):
        print(colorclass.Color("{higreen}["+POSITIVE+"]{/green}")+SEPARATOR+string)


def fail(string):
        print(colorclass.Color("{hired}["+NEGATIVE+"]{/red}")+SEPARATOR+string)


def tentative(string):
        print(colorclass.Color("{hiyellow}["+NEUTRAL+"]{/yellow}")+SEPARATOR+string)
