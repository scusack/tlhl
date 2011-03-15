#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tlhl import *
from tlhl.xhtml10 import *
from tlhl.entities import *

def check(tlhl, html):
    tlhl = render(tlhl, PrettyPrinter()).show()
    assert tlhl.strip() == html, "The following do not match:\n{0}\n{1}".format(tlhl, html)

def test_css_include() :
    check((css_include, "some.css"),
          '<link media="screen, projection" href="some.css" type="text/css" rel="stylesheet" />')

    check((css_include, {'media':'print'}, "some.css"),
          '<link media="print" href="some.css" type="text/css" rel="stylesheet" />')

def test_css() :
    check((css, """
h1 {color: red; text-align: center}
"""),
          """<style type="text/css">

h1 {color: red; text-align: center}

</style>""")

    check((css, attrs("#whatever"), """
h1 {color: red; text-align: center}
"""),
          """<style type="text/css" id="whatever">

h1 {color: red; text-align: center}

</style>""")

    check((css, "h1 {color:red;}", "\nh2 {color:purple;}"),
          """<style type="text/css">
h1 {color:red;}
h2 {color:purple;}
</style>""")

def test_js_include():

    check((js_include, "some.js"),
          '<script src="some.js" type="text/javascript"></script>')

    check((js_include, attrs("#my-script"), "some.js"),
          '<script src="some.js" id="my-script" type="text/javascript"></script>')

def test_js():
    js1 = """
var hello_world = function(){
  alert('hello world!');
};

var hello_world2 = function(){
  alert('hello world2!');
};
"""
    check((js, js1),
          """<script type="text/javascript">
// <![CDATA[

var hello_world = function(){
  alert('hello world!');
};

var hello_world2 = function(){
  alert('hello world2!');
};

// ]]>
</script>""")

    check((js, attrs("#my-id"), js1),
          """<script id="my-id" type="text/javascript">
// <![CDATA[

var hello_world = function(){
  alert('hello world!');
};

var hello_world2 = function(){
  alert('hello world2!');
};

// ]]>
</script>""")


    check((js, attrs("#my-id and-class"), js1, js1),
          """<script id="my-id" class="and-class" type="text/javascript">
// <![CDATA[

var hello_world = function(){
  alert('hello world!');
};

var hello_world2 = function(){
  alert('hello world2!');
};

var hello_world = function(){
  alert('hello world!');
};

var hello_world2 = function(){
  alert('hello world2!');
};

// ]]>
</script>""")

STRING_WITH_UTF8_CHARS =  "UTF-8 Quotes used here: “something to quote” but string just a raw string, treated as a sequence of bytes."
UNICODE_STRING_1       = u"UTF-8 Quotes used here “something to quote” encoded into a python UnicodeString."
UNICODE_STRING_2       = u"More “quoted stuff” is here."

def test_escaping():
    check((p, STRING_WITH_UTF8_CHARS),
          "<p>UTF-8 Quotes used here: “something to quote” but string just a raw string, treated as a sequence of bytes.</p>")

    check((p, UNICODE_STRING_1),
          "<p>UTF-8 Quotes used here &#8220;something to quote&#8221; encoded into a python UnicodeString.</p>")

    check((p, attrs(one=UNICODE_STRING_2), "text"),
          "<p one=\"More &#8220;quoted stuff&#8221; is here.\">text</p>")

    check((p, {UNICODE_STRING_2:UNICODE_STRING_2}, "text"),
          "<p More &#8220;quoted stuff&#8221; is here.=\"More &#8220;quoted stuff&#8221; is here.\">text</p>")

if __name__ == '__main__' :
    test_escaping()
