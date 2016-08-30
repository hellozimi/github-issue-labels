import argparse
import os
import struct
import sys

from . import config

def get_access_token():
    """ Gets the stored token in config.__token_file__ """
    try:
        with open(config.__token_file__, 'r') as f:
            return f.read().rstrip()
    except FileNotFoundError as e:
        print('🚫  You seem to be unauthenticated. Please run $ ghl auth '
              '<token> again.')
        sys.exit(1)

def parse_validation_error(name, error):
    """ Parses github error and returns proper error messages

    Args:
        name: label name
        error: error dict from github json

    Returns:
        Error message or None
    """

    if error['code'] == 'already_exists':
        return '🚫  The name \'{}\' already exists.'.format(name)
    elif error['code'] == 'invalid':
        return '🚫  The field \'{}\' is invalid.'.format(error['field'])

    return None

def text_color(color):
    """ Calculates hex color to determine monochrome value and returns
        proper text color.

    Args:
        color: string in hex

    Returns:
        String with either black or white
    """

    (r, g, b) = struct.unpack('BBB', bytes.fromhex(color))
    a = 1 - (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if a > 0.5:
        return 'white'
    return 'black'

def color_validation(value):
    """ Color validation for argument value.

    Raises Argument error or returns the passed value.

    Returns:
        The unmodified passed value

    """

    if len(value) != 6:
        raise argparse.ArgumentTypeError('Color must be 6 characters long'
                                         'without # or 0x')
    return value
