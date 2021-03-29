from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="pycrawl",
    version="3.1.0",
    description="A simple crawling utility for Python",
    license="MIT",
    author="averak",
    packages=find_packages(),
    package_data={},
    install_requires=["mechanize", "lxml", "cssselect"],
    long_description=long_description,
    keywords="crawling scraping spider",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
