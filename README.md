PyCrawl
=======

A simple crawling utility for Python

## Description

This project enables site crawling and data extraction with xpath and css selectors.
You can also send forms such as text data, files, and checkboxes.


## Requirement
- Python3


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

# get <table> tags as dict
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
1. Specify target node's attribute
2. Specify value(int or str) / check(bool) / file_name(str)
3. call submit() method with form attribute specified
```python
# login
doc.send(id='id attribute', value='value to send')
doc.send(id='id attribute', value='value to send')
doc.submit(id='id attribute') # submit

# post file
doc.send(id='id attribute', file_name='target file name')

# checkbox
doc.send(id='id  attribute', check=True)  # check
doc.send(id='id  attribute', check=False) # uncheck

# example of specify other attribute
doc.send(class_='class attribute', value=100)
doc.send(name='name attribute', value='hello')
```


## Installation
```sh
$ pip install pycrawl
```

## Contributing
Bug reports and pull requests are welcome on GitHub at [https://github.com/AjxLab/PyCrawl](https://github.com/AjxLab/PyCrawl).