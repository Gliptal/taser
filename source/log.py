from colorclass import Color as colorize


def success(string):
        print(colorize("{higreen}[+]{/green}    "+string))

def fail(string):
        print(colorize("{hired}[-]{/red}    "+string))

def tentative(string):
        print(colorize("{hiyellow}[?]{/yellow}    "+string))
