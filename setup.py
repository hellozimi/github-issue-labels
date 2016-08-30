from setuptools import setup
from ghl import __version__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ghl',
    version=__version__,
    description='Github issue label manager',
    long_description=readme,
    url='https://github.com/hellozimi/github-issue-labels',
    author='Simon Andersson',
    author_email='simon@hiddencode.me',
    license=license,
    py_modules=['ghl'],
    install_requires=[
        'requests',
        'colored',
        'x256'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': ['ghl = ghl.core:run']
    }
)
