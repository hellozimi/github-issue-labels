# Github Label Manager

A CLI to manage labels on your github repos.

## Todo

- [ ] Update label
- [ ] Bulk remove labels
- [ ] Remove all labels
- [ ] Bulk add labels
- [ ] Pass `random` to the --color argument
- [x] Pass blue/white/red/* generic named color) to --color
- [x] Create setup.py script/executable
- [ ] Windows & Linux support
- [ ] Lower python version

## Usage

First go to [Settings > Personal access tokens](https://github.com/settings/tokens) and generate a new token with at least the `repo` scope.

```
$ python setup.py install
$ glm auth <personal github token> # Authenticates with github
$ glm list hellozimi/github-label-manager # lists all labels
```

## Documentation

```
$ python glm.py --help
usage: glm [-h] {auth,list,create,delete} ...

Github Label Manager, helps managing your github issue labels.

positional arguments:
  {auth,list,create,delete}
    auth                Authenticate glm with your personal access token
                        obtained at https://github.com/settings/tokens. This
                        step is required for the program to work.
    list                List all labels in repository.
    create              Create label with name and color
    delete              Delete label from repository.

optional arguments:
  -h, --help            show this help message and exit

Source: https://github.com/hellozimi/github-label-manager
```

## Development

Prerequisite:

* Python 3.5
* Virtualenv
* Pip

```
$ git clone git@github.com:hellozimi/github-label-manager && cd github-label-manager
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Happy development.

## Other

I more than welcome pull requests, discussion and improvements to this project.

If you want to follow me you can do it on:

Twitter: [@hellozimi](https://twitter.com/hellozimi)
Instagram: [@hellozimi](https://instagram.com/hellozimi)
