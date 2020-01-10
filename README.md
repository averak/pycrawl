PyCrawl
=======

A simple crawling utility for Python

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
# get current url
doc.url
# get current site's html
doc.html
# get <table> tag's data as dict
doc.tables
# ex) doc.tables['予約・お問い合わせ'] => 050-5596-6465
```

### Scraping Example
```python
# search for nodes by css
doc.css('div')
doc.css('.main-text')
doc.css('#tadjs')

# search for nodes by xpath
doc.xpath('//*[@id="top"]/div[1]')

# other example
doc.css('div').css('a')[2].attr('href') # => string object
doc.css('p').innerText() # => string object
# You do not need to specify "[]" to access the first index
```

### Submitting Form Example
```python
doc.send(name='email', value='test@test.com')
doc.send(id='password', value='11111111')
doc.submit(name='loginForm')
```


## Installation
```sh
$ pip install pycrawl
```