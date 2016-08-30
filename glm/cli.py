import argparse
import sys

_parser = None
_subparser = None


def init(*args, **kwargs):
    """ Initializes parser and subparser.

    Args:
        args: List of arguments mirrored to argparser.ArgumentParser
        kwargs: Dict of arguments mirrored to argparser.ArgumentParser

    """

    global _parser
    global _subparser
    _parser = argparse.ArgumentParser(
        *args, **kwargs
    )
    _subparser = _parser.add_subparsers()


def parse():
    """ Parses arguments using argparse """
    if _parser is None:
        raise AssertionError('Parser not initialized')
    args = _parser.parse_args()
    if len(sys.argv[1:]) > 0:
        args.func(args)
    else:
        _parser.print_help()


class Command(object):
    """ The command proxy object.

    Used to store argparser subparser values in it.

    Attributes:
        arguments: list
        func: the callback function

    """

    pass


def _create_command(func, arguments=None, callback=None):
    """ Creates command proxy and sets passed values

    Args:
        func: The wrapped parameter from the decorator
        arguments: List of tuples from the argument decorator
        callback: The func to be set as default in argparser

    Returns:
        A proxy Command object

    """

    if not isinstance(func, Command):
        func = Command()

    if arguments is not None:
        if hasattr(func, 'arguments'):
            func.arguments.append(arguments)
        else:
            func.arguments = [arguments]

    if not hasattr(func, 'func'):
        func.func = callback

    return func


def command(*args, **kwargs):
    """ Adds a parser to the subparser """

    def wrapped(func):

        if not isinstance(func, Command):
            func = _create_command(func, callback=func)

        com = _subparser.add_parser(
            *args, **kwargs
        )
        if hasattr(func, 'arguments'):
            arguments = func.arguments
            for arg in arguments:
                com.add_argument(*arg[0], **arg[1])
        com.set_defaults(func=func.func)
        return com
    return wrapped


def argument(*args, **kwargs):
    """ Adds an argument to the Command object"""

    def wrapped(func):
        opts = (args, kwargs)
        func = _create_command(func, arguments=opts, callback=func)
        return func
    return wrapped
