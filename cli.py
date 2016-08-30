import argparse

_parser = None
_subparser = None


def init(*args, **kwargs):
    global _parser
    global _subparser
    _parser = argparse.ArgumentParser(
        *args, **kwargs
    )
    _subparser = _parser.add_subparsers()


def parse():
    args = _parser.parse_args()
    args.func(args)


class Command(object):
    pass


def _create_command(func, arguments=None, callback=None):

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
    def wrapped(func):
        opts = (args, kwargs)
        func = _create_command(func, arguments=opts, callback=func)
        return func
    return wrapped
