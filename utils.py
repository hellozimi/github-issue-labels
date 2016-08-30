import argparse
import struct


def parse_validation_error(name, error):
    if error['code'] == 'already_exists':
        return '🚫  The name \'{}\' already exists.'.format(name)
    elif error['code'] == 'invalid':
        return '🚫  The field \'{}\' is invalid.'.format(error['field'])

    return None

def text_color(color):
    (r, g, b) = struct.unpack('BBB', bytes.fromhex(color))
    a = 1 - (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if a > 0.5:
        return 'white'
    return 'black'

def color_validation(value):
    if len(value) != 6:
        raise argparse.ArgumentTypeError('Color must be 6 characters long'
                                         'without # or 0x')
    return value
