#!/usr/bin/env python

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


if __name__ == '__main__' :
    test_js_include()
