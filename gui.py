"""
Module to create graphical backdrops
"""

from PIL import Image
from numpy import asarray

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
    print(terminal_command[command])


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

    # Hide cursor and blat with no new line at end
    terminal_control("cursor_home")
    terminal_control("hide_cursor")
    print(gui_image, end="")
