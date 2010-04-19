#!/usr/bin/env python

import datetime

from tlhl import *
from tlhl.xhtml10 import *
from tlhl.entities import *

def example_1() :
    """
    Things to note:

    * Unicode called on date in title so string representation is printed.

    * Default attribute values for the script tag.

    * Selected attribute is rendered as selected="selected"
    """

    doc = (html,
           (head,
            (title, "Example generated on: ", datetime.date.today()),
            (script, dict(src="example-javascript.js"))),
           (body,
            (select, attrs("#a-select fancy-drop-down"),
             [(option, attrs(selected=idx==4), "option {0}".format(idx)) for idx in range(10)])))
    print render(doc, PrettyPrinter()).show()

def example_2() :
    """
    Things to note:

    * Custom attributes that get escaped.

    * Classes key parameter to attrs treated sepcially.

    * UL contains both static and dynamic content.

    * Escaped <>& characters in output.

    * More complex attrs id/class specifications.
    """
    doc = (html, {},
           (head, {},
            (css_include, "/assets/whatever.css"),
            (css, """
body {
  background-color : white;
}
"""),
            (js, """
var afunc = function(param1, param2){
  if (param1 && param2) {
    return 'woohoo the ampersands didn't get escaped!';
  }
  return 'doh!!!'
};
""")),
           (body, attrs(classes=["soria", "content"],
                        custom="this>should<get?escaped?''<fingers crossed"),
            (ul, dict(style="text-align:right;", number_attr=10),
             [(li, "item {0}".format(idx + 1)) for idx in range(10)],
             (li, "this is a static thing"),
             (li, "this is a number:", NBSP, 100, "!"),
             [(li, "item {0}".format(idx + 11)) for idx in range(10)],
             (li, "and then a bit more stuff with some embedded <>& things")),
            (div, attrs("#something-or-other with some more classes"),
             "this is some content",
             "")))
    print render(doc, PrettyPrinter()).show()

def example_3():
    """
    Things to note:

    * id and class values for the paragraphs
    """
    doc = (body,
           (p, attrs("#my-id class1 class2", classes=['classA', 'classB']),
            "Then a paragraph."),
           (p, attrs(" class1 class2", classes=['classA', 'classB']),
            "Then another paragraph."),
           (p, attrs(namespace__attribute="you should see a colon in the emitted name"),
            "Then another paragraph that has a namespaced attributed."))
    print render(doc, PrettyPrinter()).show()

if __name__ == '__main__' :
    example_1()
    example_2()
    example_3()
