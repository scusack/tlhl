"""
Need to move a bunch of the html tag elements into a dialect and base it on this;

http://xhtml.com/en/xhtml/reference/
"""

from types import DictType
from base import make_block, make_inline, cdata
from entities import *

DOCTYPE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">"""

html = make_block('html', {"xmlns":"http://www.w3.org/1999/xhtml"})
head = make_block('head')
body = make_block('body')

link   = make_block('link')
css    = make_block('link',   {"type":"text/css", "rel":"stylesheet"})
script = make_block('script', {"type":"text/javascript"}, explicit_end_p=True)
style  = make_block('style',  {"type":"text/css"}, explicit_end_p=True)
title  = make_block('title')

h1 = make_block('h1', explicit_end_p=True)
h2 = make_block('h2', explicit_end_p=True)
h3 = make_block('h3', explicit_end_p=True)
h4 = make_block('h4', explicit_end_p=True)
h5 = make_block('h5', explicit_end_p=True)
h6 = make_block('h6', explicit_end_p=True)

div  = make_block('div', explicit_end_p=True)
p    = make_block('p')
br   = make_block('p')

span   = make_inline('span')
strong = make_inline('strong')
em     = make_inline('em')
a      = make_inline('a')
img    = make_inline('img')

ul   = make_block('ul')
ol   = make_block('ol')
li   = make_block('li')

select = make_block('select')
option = make_block('option')

table = make_block('table')
thead = make_block('thead')
tbody = make_block('tbody')
tr    = make_block('tr')
th    = make_block('th')
td    = make_block('td')

form     = make_block('form', {"method":"post", "action":""})
label    = make_inline('label')
input    = make_inline('input')
text     = make_inline('input', {"type":"text"})
password = make_inline('input', {"type":"password"})
hidden   = make_inline('input', {"type":"hidden"})
checkbox = make_inline('input', {"type":"checkbox"})
radio    = make_inline('input', {"type":"radio"})
submit   = make_inline('input', {"type":"submit"})
button   = make_inline('button')
