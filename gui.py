"""
Module to create graphical backdrops
"""

from PIL import Image
from numpy import asarray
from colorama import Fore, Back, Style

# Map bitmap pixel colours to equivalent escape characters
# \u2588 fills a whole character cell 
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
    "clear_screen": "\033[2J\033[2;0H",
    "hide_cursor": "\033[?25l",
    "show_cursor": "\033[?25h",
    "cursor_home": "\033[H",
    "text_blue": "\033[44;34m",
    "text_white": "\033[37m\u2588"
}


title = [
    # Put cursor home for set style and colour else renders in wrong place
    # Title created in ASCII Art generator https://patorjk.com/software/taag/
    Back.BLUE + Fore.WHITE + Style.BRIGHT + "\033[H",
    "\033[5;20H         ██████╗ ██████╗ ██████╗", 
    "\033[6;20H        ██╔════╝██╔═══██╗╚════██╗",
    "\033[7;20H        ██║     ██║   ██║ █████╔╝",
    "\033[8;20H        ██║     ██║   ██║██╔═══╝",
    "\033[9;20H        ╚██████╗╚██████╔╝███████╗",
    "\033[10;20H         ╚═════╝ ╚═════╝ ╚══════╝",
    "\033[12;20H███████╗ ██████╗ ██████╗ ██████╗ ███████╗",
    "\033[13;20H██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝",
    "\033[14;20H███████╗██║     ██║   ██║██████╔╝█████╗",
    "\033[15;20H╚════██║██║     ██║   ██║██╔══██╗██╔══╝",
    "\033[16;20H███████║╚██████╗╚██████╔╝██║  ██║███████╗",
    "\033[17;20H╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝",
    "\033[19;20H       Calculate your co2 score"
]


class GuiImage:
    """
    Creates an instance of a GUI image for reading
    """
    def __init__(self, pixel_array, image_size, image_array):
        self.pixel_array = pixel_array
        self.image_size = image_size
        self.image_array = image_array


def terminal_control(command):
    """
    Takes a passed command and prints required
    escape character to screen to action the command
    """
    print(terminal_command[command], end="")


def open_image(image_name):
    """
    Opens the requested image for use
    """
    with Image.open(image_name) as image:
        pixel_array = image.load()
        image_size = image.size
        image_array = asarray(image)
    gui_image = GuiImage(pixel_array, image_size, image_array)
    return gui_image


def set_gui_background(requested_background):
    """
    Translate bitmap pixels to escape characters and print to screen
    """
    image_map = open_image(requested_background)
    gui_image = ""
    for pixel_row in range(int(image_map.image_size[1])):
        for pixel_col in range(int(image_map.image_size[0])):
            # Run next command twice as two terminal char cells 
            # are roughly square matching bitmap pixel shape
            gui_image += colour_map[str(image_map.pixel_array
                                        [pixel_col, pixel_row])] * 2
            if pixel_col == 39 and pixel_row <= 22:
                gui_image += "\n"

    # Hide cursor and print to screen with no new line at end
    terminal_control("clear_screen")
    terminal_control("cursor_home")
    terminal_control("hide_cursor")
    print(gui_image, end="")


def app_title():
    """
    Define and print the app title to screen
    """
    for string in title:
        print(string)
