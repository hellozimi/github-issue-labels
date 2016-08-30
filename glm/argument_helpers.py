from . import utils


class Argument(dict):

    def __init__(self, **kwargs):
        keys = [x for x in list(set(dir(self)) - set(dir(dict)))
                if not x.startswith('__')]

        for key in keys:
            attr = getattr(self, key)
            if hasattr(attr, '__call__'):
                self[key] = attr()
            else:
                self[key] = attr

        self.update(kwargs)



class RepoArg(Argument):
    metavar = '<username/repo>'
    def type(self):
        return utils.repository_validation


class ColorArg(Argument):
    metavar = '<color>'

    def type(self):
        return utils.color_validation


class ShowColorArg(Argument):
    default = False
    action = 'store_true'
    help = 'Pass to show hex color code in list.'


class NameArg(Argument):
    nargs = '+'
    metavar = '<label name>'
