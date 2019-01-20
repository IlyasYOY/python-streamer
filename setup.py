from os.path import join, dirname

from setuptools import setup, find_packages

import streamer

setup(
    name='pyperstream',
    version=streamer.__version__,
    author="Ilia Ilinykh",
    author_email="ilyasyoy@gmail.com",
    description="A small simple Stream API-like wrapper.",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IlyasYOY/python-streamer",
    test_suite='test'
)
