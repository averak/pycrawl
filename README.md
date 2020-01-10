PyCrawl
=======

Script for crawling in Python.

## Description

This project enables site crawling and data extraction with xpath and css selectors.
You can also send forms such as text data, files, and checkboxes.


## Requirement

- Python3
- mechanize
- lxml


## Usage
### Simple Example
```python
import pycrawl

url = 'http://www.example.com/'
doc = pycrawl.PyCrawl(url)

# access another url
doc.get('another url')
```

## Scraping Example
```python
# Search for nodes by css
doc.css('div')
doc.css('.main-text')
doc.css('#tadjs')

# Search for nodes by xpath
doc.xpath('//*[@id="top"]/div[1]')

# Other Example
doc.css('div').css('a')[2].attr('href') # => String Object
doc.css('p').innerText() # => String Object
doc.tables  # -> Table Tag to Dict

# You do not need to specify "[]" to access the first index
```


## Installation
```sh
$ pip install pycrawl
```