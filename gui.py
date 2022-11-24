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
    def __inti__(self, pixel_array, image_size, image_array):
        self.pixel_array = pixel_array
        self.image_size = image_size
        self.image_array = image_array


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
