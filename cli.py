import argparse
import sys

parser = None
def init(*args, **kwargs):
    parser = argparse.ArgumentParser(
        *args, **kwargs
    )

class Command(object):
    pass


def command(*args, **kwargs):
    def wrapped(func):
        subparser = parser.add_subparsers()
        com = subparser.add_parser(
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
    def wrapped(func):
        opts = (args, kwargs)
        callback = func

        if not isinstance(func, Command):
            func = Command()

        if hasattr(func, 'arguments'):
            func.arguments.append(opts)
        else:
            func.arguments = [opts]

        if not hasattr(func, 'func'):
            func.func = callback
        return func
    return wrapped
