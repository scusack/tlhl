"""
Need to move a bunch of the html tag elements into a dialect and base it on this;

http://xhtml.com/en/xhtml/reference/
"""

from types import DictType
from base import renderer, make_block, make_inline, raw
from entities import *

# Declarations

DOCTYPE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">"""

# Structure & Header Elements

base   = make_block('base', has_content_p=False)
body   = make_block('body')
head   = make_block('head')
html   = make_block('html', {"xmlns":"http://www.w3.org/1999/xhtml"})
link   = make_block('link')
meta   = make_block('meta', has_content_p=False)
script = make_block('script', {"type":"text/javascript"}, explicit_end_p=True)
style  = make_block('style',  {"type":"text/css"},        explicit_end_p=True)
title  = make_block('title')

# - convenient wrappers for some common usage patterns
def consume_attrs(params, attrs):
    if isinstance(params[0], DictType):
        attrs.update(params[0])
        return params[1:], attrs
    return params, attrs

@renderer
def css(params, printer):
    """
    Include link to an external CSS resource.

    Usage:

    (css, "some-stylesheet.css")

    or

    (css, {"media" : "print"}, "some-stylesheet.css")

    Only the first two parameters are considered significant.
    """

    params, attrs = consume_attrs(params,
                                  {"type"  : "text/css",
                                   "rel"   : "stylesheet",
                                   "media" : "screen, projection"})
    if len(params) != 1 :
        raise TypeError("Too many parameters passed to 'css' renderer: %s", params)

    attrs['href'] = params[0]

    return (link, attrs)

@renderer
def stylesheet(params, printer):
    """
    Inline stylesheet.

    Usage:

    (stylesheet, "h1 {color:red;}", "h2 {color:purple;}")
    """
    params, attrs = consume_attrs(params, {"type":"text/css"})
    return (style, attrs, (raw, "\n", params, "\n"))

@renderer
def js(params, printer):
    """
    Shorthand to include javascript via src link

    Usage:

    (js, "/assets/some.js")
    """
    params, attrs = consume_attrs(params, {})
    if len(params) != 1 :
        raise TypeError("Too many parameters pass to 'js' renderer: %s", params)

    attrs["src"] = params[0]
    return (script, attrs)

@renderer
def javascript(params, printer):
    """
    Emits the contents (which are assumed to be valid javascript to
    the printer, wrapped in a CDATA section.

    Usage:
    (js, "var hello_world = function() { alert('hello world');};")

    or:

    (js,
    "var hello_world = function() { alert('hello world');};",
    "var hello_world2 = function() { alert('hello world2');};",
    )
    """

    params, attrs = consume_attrs(params, {})
    return (script, attrs,
            (raw,
             '\n// <![CDATA[\n',
             params,
             '\n// ]]>\n'))


# Block Elements

address    = make_block('address')
blockquote = make_block('blockquote')
del_       = make_block('del', explicit_end_p=True)
div        = make_block('div', explicit_end_p=True)
dl         = make_block('dl')
fieldset   = make_block('fieldset')
form       = make_block('form', {"method":"post", "action":""})
h1         = make_block('h1', explicit_end_p=True)
h2         = make_block('h2', explicit_end_p=True)
h3         = make_block('h3', explicit_end_p=True)
h4         = make_block('h4', explicit_end_p=True)
h5         = make_block('h5', explicit_end_p=True)
h6         = make_block('h6', explicit_end_p=True)
hr         = make_block('hr')
ins        = make_block('ins')
noscript   = make_block('noscript')
ol         = make_block('ol')
p          = make_block('p')
pre        = make_block('pre')
table      = make_block('table')
ul         = make_block('ul')


# Inline Elements

a        = make_inline('a')
abbr     = make_inline('abbr')
acronym  = make_inline('acronym')
b        = make_inline('b')
bdo      = make_inline('bdo')
big      = make_inline('big')
br       = make_inline('br')
button   = make_inline('button')
cite     = make_inline('cite')
code     = make_inline('code')
dfn      = make_inline('dfn')
em       = make_inline('em')
i        = make_inline('i')
img      = make_inline('img')
ins      = make_inline('ins')
input    = make_inline('input')
label    = make_inline('label')
map_     = make_inline('map')
kbd      = make_inline('kbd')
object_  = make_inline('object')
q        = make_inline('q')
ruby     = make_inline('ruby')
samp     = make_inline('samp')
select   = make_block('select')
small    = make_inline('small')
span     = make_inline('span')
strong   = make_inline('strong')
sub      = make_inline('sub')
sup      = make_inline('sup')
textarea = make_inline('textarea')
tt       = make_inline('tt')
var      = make_inline('var')

# - extra useful inline inputs
text     = make_inline('input', {"type":"text"})
password = make_inline('input', {"type":"password"})
hidden   = make_inline('input', {"type":"hidden"})
checkbox = make_inline('input', {"type":"checkbox"})
radio    = make_inline('input', {"type":"radio"})
submit   = make_inline('input', {"type":"submit"})

# List Item Elements

dd = make_block('dd')
dt = make_block('dt')
li = make_block('li')

# Table Content Elements

caption  = make_block('caption')
col      = make_block('col')
colgroup = make_block('colgroup')
tbody    = make_block('tbody')
td       = make_block('td')
tfoot    = make_block('tfoot')
th       = make_block('th')
thead    = make_block('thead')
tr       = make_block('tr')

# Form Fieldset Legends

legend = make_block('legend')

# Form Menu Options

optgroup = make_block('optgroup')
option   = make_block('option')

# Map Areas

area = make_inline('area')

# Object Parameters

param = make_inline('param')

# Ruby Annotations

rb  = make_inline('rb')
rbc = make_inline('rbc')
rp  = make_inline('rp')
rt  = make_inline('rt')
rtc = make_inline('rtc')
