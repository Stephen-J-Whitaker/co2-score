"""
Module to create graphical backdrops
"""

from PIL import Image
from numpy import asarray
from colorama import Fore, Back, Style

# Map bitmap pixel colours to equivalent escape characters
colour_map = {
    "(0, 0, 0)": "\033[40;30m\u2588",  # black
    "(255, 0, 0)": "\033[41;31m\u2588",  # red
    "(0, 255, 0)": "\033[42;32m\u2588",  # green
    "(255, 255, 0)": "\033[43;33m\u2588",  # yellow
    "(0, 0, 255)": "\033[44;34m\u2588",  # blue
    "(255, 0, 255)": "\033[45;35m\u2588",  # magenta
    "(0, 255, 255)": "\033[46;36m\u2588",  # cyan
    "(255, 255, 255)": "\033[47;37m\u2588"  # white
}

# Terminal command to escape character map
terminal_command = {
    "clear_screen": "\033[2J",
    "hide_cursor": "\033[?25l",
    "show_cursor": "\033[?25h",
    "cursor_home": "\033[H"
}


