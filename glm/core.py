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

from . import cli
from . import utils

from .config import (
    __github_url__,
    __token_file__
)


""" Initialize cli program """
cli.init(
    prog='glm',
    description='''Github label manager, helps managing your github issue
                    labels.''',
    epilog="Source: https://github.com/hellozimi/github-label-manager"
)


@cli.command(
    'auth',
    help='''Authenticate glm with your personal access token obtained at
            https://github.com/settings/tokens. This step is required for the
            program to work.'''
)
@cli.argument(
    'token',
    action='store',
    help='Github personal access token.',
    metavar='<access token>'
)
def auth_command(args):
    """ Parses the authentication command.
    Stores a file at __token_file__ with the personal access token in it.

    Args:
        args: Object with a personal github token string in it
    """

    f = open(__token_file__, 'w', encoding='utf-8')
    print(args.token, file=f)
    f.close()
    print('🚀  Authentication stored!')


@cli.command(
    'list',
    help='List all labels in repository.'
)
@cli.argument(
    'repo',
    help='The repository you want to list labels from.',
    metavar='<username/repo>'
)
@cli.argument(
    '--show-colors',
    default=False,
    action='store_true',
    help='Pass to show hex color code in list.'
)
def list_command(args):
    """ Parses the list command.
    Fetches the target repositry passed in args and prints a colored list

    Args:
        args: Object with repo in it

    """

    params = {'access_token': utils.get_access_token()}

    url = '{}/repos/{}/labels'.format(__github_url__, args.repo)
    r = requests.get(url, params=params)
    res = r.json()

    if len(res) == 0:
        print("❗️  No labels found")
        sys.exit(0)

    spacing = len(max([x['name'] for x in res], key=len))
    for row in res:
        name = row['name']
        c = row['color']
        fmt = '{}{} {} {} {}'.format(
            bg(x256.from_hex(c)),
            fg(utils.text_color(c)),
            name.center(spacing),
            attr(0),
            '[#{}]'.format(c) if args.show_colors else '',
        )
        print(fmt)


@cli.command(
    'create',
    help='Create label with name and color'
)
@cli.argument(
    'repo',
    metavar='<username/repo>',
    help='The repository you want to add labels to.'
)
@cli.argument(
    '--name',
    nargs='+',
    required=True,
    help='Name of the label you want to create.',
    metavar='<name>'
)
@cli.argument(
    '--color',
    required=True,
    help='Color of the label you want to create in hex without # or 0x.',
    metavar='<color>',
    type=utils.color_validation
)
def create_command(args):
    """ Parses the create command.
    Creates a new label at the wanted location.

    Args:
        args: Object with repo, name and color in it

    """

    params = {'access_token': utils.get_access_token()}
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
                errors.append(utils.parse_validation_error(name, error))

        if len(errors) == 0:
            errors.append("❌  Failed to create label.")

        print('\n'.join(errors))


@cli.command(
    'delete',
    help='Delete label from repository.'
)
@cli.argument(
    'repo',
    metavar='<username/repo>',
    help='The repository you want to add labels to.'
)
@cli.argument(
    'name',
    nargs='+',
    metavar='<label name>',
    help='The name of the label you want to delete.'
)
@cli.argument(
    '-f', '--force',
    default=False,
    action='store_true',
    help='Pass --force if you don\'t want to confirm your action'
)
def delete_command(args):
    """ Parses the delete command.
    Deletes a label at the wanted location. Ask for confirmation unless
        -f/--force is passed

    Args:
        args: Object with repo and name in it. Optionally force as boolean.

    """

    name = ' '.join(args.name)
    question = '⛔️  Are you sure you want to delete \'{}\'?'.format(name)
    prompt = ' [y/N] '
    while not args.force:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '' or choice == 'n' or choice == 'no':
            return
        elif choice == 'y' or choice == 'yes':
            break

    params = {'access_token': utils.get_access_token()}
    url = '{}/repos/{}/labels/{}'.format(__github_url__, args.repo, name)
    r = requests.delete(url, params=params)
    if r.status_code == 204:
        print("🗑  Label successfully removed")
    elif r.status_code == 404:
        msg = '🚫  The label \'{}\' doesn\'t exist in {}.'.format(
            name,
            args.repo
        )
        print(msg)
    else:
        print("❌  Failed to create label.")


def run():
    cli.parse()
