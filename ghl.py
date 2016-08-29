import argparse
import os
import sys
import struct

import requests

from colored import (
    fg,
    bg,
    attr
)
from x256 import x256


__token_file_name__ = '.ghl-token'
__token_file__ = os.path.join(os.path.expanduser('~'), __token_file_name__)
__github_url__ = 'https://api.github.com'


def get_access_token():
    with open(__token_file__, 'r') as f:
        return f.read().rstrip()


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


def parse_validation_error(name, error):
    if error['code'] == 'already_exists':
        return '🚫  The name \'{}\' already exists.'.format(name)
    elif error['code'] == 'invalid':
        return '🚫  The field \'{}\' is invalid.'.format(error['field'])

    return None

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()


def auth_command(args):
    f = open(__token_file__, 'w', encoding='utf-8')
    print(args.token, file=f)
    f.close()
    print('🚀  Authentication stored!')

auth_parser = subparser.add_parser('auth')
auth_parser.add_argument(
    'token',
    action='store',
    help='Github personal access token'
)
auth_parser.set_defaults(func=auth_command)


def list_command(args):
    params = {'access_token': get_access_token()}

    url = '{}/repos/{}/labels'.format(__github_url__, args.repo)
    r = requests.get(url, params=params)
    res = r.json()

    spacing = len(max([x['name'] for x in res], key=len))
    for row in res:
        name = row['name']
        c = row['color']
        fmt = '{}{} {} {} {}'.format(
            bg(x256.from_hex(c)),
            fg(text_color(c)),
            name.center(spacing),
            attr(0),
            '[#{}]'.format(c) if args.show_colors else '',
        )
        print(fmt)

list_parser = subparser.add_parser('list')
list_parser.add_argument(
    'repo',
    help='The owner and repo combined with a slash'
)
list_parser.add_argument('--show-colors', default=False, action='store_true')
list_parser.set_defaults(func=list_command)


def create_command(args):
    params = {'access_token': get_access_token()}
    name = ' '.join(args.name)
    payload = {
        'name': name,
        'color': args.color
    }

    url = '{}/repos/{}/labels'.format(__github_url__, args.repo)
    r = requests.post(url, json=payload, params=params)

    if r.status_code == 201:
        print("✅  Label successfully created")
    else:
        res = r.json()
        errors = []
        if 'Validation Failed' in res.get('message', ''):
            for error in res.get('errors', []):
                errors.append(name, parse_validation_error(error))

        if len(errors) == 0:
            errors.append("❌  Failed to create label")

        print('\n'.join(errors))


create_parser = subparser.add_parser('create')
create_parser.add_argument('repo')
create_parser.add_argument('--name', nargs='*', required=True)
create_parser.add_argument('--color', required=True, type=color_validation)
create_parser.set_defaults(func=create_command)


def delete_command(args):
    question = '⛔️  Are you sure you want to delete \'{}\'?'.format(args.name)
    prompt = ' [y/N] '
    while not args.force:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '' or choice == 'n' or choice == 'no':
            return
        elif choice == 'y' or choice == 'yes':
            break

    params = {'access_token': get_access_token()}
    url = 'https://api.github.com/repos/{}/labels/{}'.format(args.repo,
            args.name)
    r = requests.delete(url, params=params)
    if r.status_code == 204:
        print("🗑  Label successfully removed")
    elif r.status_code == 404:
        msg = '🚫  The label \'{}\' doesn\'t exist in {}.'.format(
            args.name,
            args.repo
        )
        print(msg)
    else:
        print("❌  Failed to create label")


delete_parser = subparser.add_parser('delete')
delete_parser.add_argument('repo')
delete_parser.add_argument('name')
delete_parser.add_argument('--force', default=False, action='store_true')
delete_parser.set_defaults(func=delete_command)

args = parser.parse_args()
args.func(args)
