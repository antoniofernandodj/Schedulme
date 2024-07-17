def print_yellow(string: str, **kwargs):
    print("\033[93m{}\033[0m".format(string), **kwargs)


def print_green_bright(string: str, **kwargs):
    print("\033[92;1m{}\033[0m".format(string), **kwargs)


def print_cyan_bright(string: str, **kwargs):
    print("\033[96;1m{}\033[0m".format(string), **kwargs)


def print_red(string: str, **kwargs):
    print("\033[91m{}\033[0m".format(string), **kwargs)


def print_blue(string: str, **kwargs):
    print("\033[94m{}\033[0m".format(string), **kwargs)


def print_magenta(string: str, **kwargs):
    print("\033[95m{}\033[0m".format(string), **kwargs)


def print_cyan(string: str, **kwargs):
    print("\033[96m{}\033[0m".format(string), **kwargs)


def print_white(string: str, **kwargs):
    print("\033[97m{}\033[0m".format(string), **kwargs)


def print_black(string: str, **kwargs):
    print("\033[30m{}\033[0m".format(string), **kwargs)


def print_bold(string: str, **kwargs):
    print("\033[1m{}\033[0m".format(string), **kwargs)


def print_underline(string: str, **kwargs):
    print("\033[4m{}\033[0m".format(string), **kwargs)


def print_inverse(string: str, **kwargs):
    print("\033[7m{}\033[0m".format(string), **kwargs)


def print_reset(string: str, **kwargs):
    print("\033[0m{}\033[0m".format(string), **kwargs)


def print_bold_red(string: str, **kwargs):
    print("\033[91;1m{}\033[0m".format(string), **kwargs)


def print_bold_green(string: str, **kwargs):
    print("\033[92;1m{}\033[0m".format(string), **kwargs)


def print_bold_yellow(string: str, **kwargs):
    print("\033[93;1m{}\033[0m".format(string), **kwargs)


def print_bold_blue(string: str, **kwargs):
    print("\033[94;1m{}\033[0m".format(string), **kwargs)


def print_bold_magenta(string: str, **kwargs):
    print("\033[95;1m{}\033[0m".format(string), **kwargs)


def print_bold_cyan(string: str, **kwargs):
    print("\033[96;1m{}\033[0m".format(string), **kwargs)


def print_underline_red(string: str, **kwargs):
    print("\033[91;4m{}\033[0m".format(string), **kwargs)


def print_underline_green(string: str, **kwargs):
    print("\033[92;4m{}\033[0m".format(string), **kwargs)


def print_underline_blue(string: str, **kwargs):
    print("\033[94;4m{}\033[0m".format(string), **kwargs)


def print_inverse_cyan(string: str, **kwargs):
    print("\033[96;7m{}\033[0m".format(string), **kwargs)
