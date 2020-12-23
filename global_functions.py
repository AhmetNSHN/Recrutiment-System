class user:

    def __init__(self,username, first, last):
        self.global_username = username
        self.global_fname = first
        self.global_lname = last

    def __str__(self):
        return f"{self.global_username}"


def center_screen_geometry(screen_width, screen_height, window_width, window_height):
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    return f"{window_width}x{window_height}+{x}+{y}"


def days():
    values = []
    for value in range(0, 31):
        values.append(value)
    return values


def months():
    values = []
    for value in range(0, 13):
        values.append(value)
    return values


def years():
    values = []
    for value in range(1950, 2020):
        values.append(value)
    return values

def future_years():
    values = []
    for value in range(2020, 2035):
        values.append(value)
    return values

def hour():
    values = []
    for value in range(0, 25):
        values.append(value)
    return values


def minute():
    values = []
    for value in range(0, 61):
        values.append(value)
    return values