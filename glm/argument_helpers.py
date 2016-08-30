from . import utils


class Argument(dict):

    def __init__(self, **kwargs):
        keys = [x for x in dir(self) if not callable(getattr(self, x))
                                        and not x.startswith('__')]
        for key in keys:
            self[key] = getattr(self, key)

        self.update(kwargs)


class RepoArg(Argument):
    metavar = '<username/repo>'
    type = utils.repository_validation


class ColorArg(Argument):
    metavar = '<color>'
    type = utils.color_validation


class ShowColorArg(Argument):
    default = False
    action = 'store_true'
    help = 'Pass to show hex color code in list.'


class NameArg(Argument):
    nargs = '+'
    metavar = '<label name>'
