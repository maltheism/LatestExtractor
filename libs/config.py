import os
import sys


class Settings:
    def __init__(self):
        pass

    # url of loris instance.
    url = 'https://awickenheiser-dev.loris.ca'
    # username for loris.
    username = 'admin'
    # password for loris.
    password = 'a1123581321'
    # enable debug mode.
    debug = True

    # disables print if debug false.
    @staticmethod
    def debugger():
        if not Settings.debug:
            # disable print.
            sys.stdout = open(os.devnull, 'w')
        else:
            # enable print.
            sys.stdout = sys.__stdout__
