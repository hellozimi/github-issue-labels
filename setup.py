from setuptools import setup
from glm import __version__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='glm',
    version=__version__,
    description='Github Label Manager',
    long_description=readme,
    url='https://github.com/hellozimi/github-label-manager',
    author='Simon Andersson',
    author_email='simon@hiddencode.me',
    license=license,
    packages=['glm'],
    py_modules=['glm'],
    install_requires=[
        'requests',
        'colored',
        'x256'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': ['glm = glm.core:run']
    }
)
