from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pycrawl',
    packages=['pycrawl'],
    install_requires=["mechanize", "lxml"],

    version='2.4.0',
    license='MIT',

    author='Tatsuya Abe',
    author_email='abe12@mccc.jp',

    url='https://github.com/AjxLab/PyCrawl',

    desription='A simple crawling utility for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='crawling crawler scraping',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
