def print_yellow(string: str):
    print("\033[93m{}\033[0m".format(string))


def print_green_bright(string: str):
    print("\033[92;1m{}\033[0m".format(string))


def print_cyan_bright(string: str):
    print("\033[96;1m{}\033[0m".format(string))
