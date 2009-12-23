#!/usr/bin/env python

# try and use the installed version first, then fallback to the one in this repo.
try :
    from tlhl import *
    from tlhl.xhtml10 import *
except :
    import sys
    sys.path.append('..')

    from tlhl import *
    from tlhl.xhtml10 import *

def example_0():
    doc = (html,
           (head, "invalid as head should not have text content (I think?)"))
    print render(doc, PrettyPrinter()).show()

def example_1() :
    doc = (html,
           (head,
            (link, "whatever")),
           (body,
            (select, attrs("#a-select fancy-drop-down"),
             [(option, attrs(selected=idx==4), "option {0}".format(idx)) for idx in range(10)]
            ),
           ))
    print render(doc, PrettyPrinter()).show()

def example_2() :
    doc = (html, {},
           (head, {},
            (css, attrs(src="/assets/whatever.css")),
            (style, (cdata, """
body {
  background-color : white;
}
""")),
            (script, (cdata, """
var afunc = function(param1, param2){
  if (param1 && param2) {
    return 'woohoo the ampersands didn't get escaped!';
  }
  return 'doh!!!'
};
"""))),
           (body, attrs(classes=["soria", "content"],
                        whatever="this>probably?''<should work"),
            (ul, dict(style="text-align:right;"),
             [(li, "item {0}".format(idx + 1)) for idx in range(10)],
             (li, "this is a custom thing"),
             [(li, "item {0}".format(idx + 11)) for idx in range(10)],
             (li, "and then a bit more stuff with some embedded <>& things")),
            (div, attrs("#something-or-other with some more classes"),
             "this is some content",
             "")))
    print render(doc, PrettyPrinter()).show()

def example_3():
    doc = (css, attrs(src="/assets/whatever.css"))
    print render(doc, PrettyPrinter()).show()

if __name__ == '__main__' :
    example_0()
    example_1()
    example_2()
    example_3()
