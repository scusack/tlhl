# TLHL - _T_he _L_ast _H_TML _L_ibrary you will ever need!

Yeah right.

## Motivation

I wanted to generate HTML without:

* Learning another language.

* Configuring my editor to understand another language.

* Dealing with the inevitable brain slowdown associated with the
  python versus template language context shift that occurs when
  swapping between writing code and writing page templates.

* Being constrained by another projects' design goals or philosophy.

I wanted a library that:

* Looks and feels natural inline in my code.

* Lets me abstract away common idioms.

* Lets me have an escape hatch to emit ugly hacks when required.

* Has a very natural feel which respects python idioms and also
  suggests the final structure.

* Produces HTML that is easy to read (not strictly necessary however I
  find well structured HTML that is easy to read a great boon for
  debugging and hence productivity).

* Can be used for producing HTML snippets to make working with
  templating systems in legacy applications less painful.

## Philosophy

Why another HTML generation library in python?

Well in no particular order in python I've used;

* [Quixote's PTL](http://www.mems-exchange.org/software/quixote/)
* [Cheetah](http://www.cheetahtemplate.org/)
* [Django](http://docs.djangoproject.com/)
* [Genshi](http://genshi.edgewall.org/)
* [Mako](http://www.makotemplates.org/)
* [lxml.html](http://codespeak.net/lxml/)

In common-lisp I've used;

* [htmlgen](http://opensource.franz.com/aserve/htmlgen.html)
* [cl-who](http://weitz.de/cl-who/)

I've written a few of my own, some in python and one in lisp.

I have come to the conclusion that templating languages are a solution
to a problem that does not exist.<strong><sup>i.</sup></strong>

But enough blabbing, where's the cheese?

    page = \
    (html,
     (head,
      (title, "Pythonic HTML generation that tries to suck only a little."),
      (css, dict(href="colour-me-happy.css"))),
     (body,
      (h1, "Something witty here..."),
      (ul,
       (li, "I can think of..."),
       [(li, number + 1) for number in range(random.randint(10, 100))],
       (li, "reasons this is better than the alternatives")),
      (p, "but I only need one:"),
      (strong, "very low impedance mismatch.")))

    print render(page, PrettyPrinter()).show()

    <html .... blah blah blah lots of redundant extra <> displayed.

    </html>

## Documentation

### Overview

HTML documents are just one way to encode hierarchical relationships
between elements.

A combination of lists, tuples, dictionaries and simple conventions
are another.

This library is just a translation from one encoding to another, ie,
python data structures to HTML.

### Detail

TLHL assumes that you will give it a data structure that conforms to
some simple conventions, it will then turn that into HTML.

Here are the conventions:

* Tuples are Elements.

  The first element of a tuple must either be an Element instance or a
  callable with a renderer_p<strong><sup>ii.</sup></strong> attribute
  which evaluates to True.

* Some Dictionaries are Element attributes.<strong><sup>iii.</sup></strong>

  If the second element of a tuple whose first element is an Element
  instance is a dictionary then it overrides and adds attributes to
  the element.

* Callables are called.

  If the first element in a tuple passes the renderer_p test then it
  is called and passed the remaining elements in the tuple as the
  first argument and the current printer as the second.

  Anything returned by the callable is treated as more content and
  converted too.

* Lists are nested content.

  Lists are a handy way of embedding dynamic content.  Python
  generators are particularly useful for this.

* _None_ and _False_ are ignored.

  This includes element attributes.

* _True_ element attributes are converted to xhtml conventions.

  For example selected=True becomes selected="selected" when emitted.

* Everything else is content.

  Anything not falling into one of the above categories gets unicode()
  called on it in preparation for output.

## Quick Examples

In the examples below some redundant noise has been removed, please
see [examples.py](examples.py) for the real deal.

### Example 1 - Hello World

This;

    (html,
      (head, (title, Hello World")),
      (body,
        (h1, "Hello World")))

becomes;

    <html>
      <head>
        <title>Hello World</title></head>
      <body>
        <h1>Hello World</h1></body></html>

## Example 2 - Hello World - dynamic content

This;

    lis = [(li, idx + 1) for idx in range(3)]

    (html,
      (head, (title, Hello World")),
      (body,
        (h1, "Hello World"),
        (ul,
          lis)))

becomes;

    <html>
      <head>
        <title>Hello World</title></head>
      <body>
        <h1>Hello World</h1>
        <ul>
          <li>1</li>
          <li>2</li>
          <li>3</li></ul></body></html>


## Common pitfalls

### Missing Commas

I find that by far the most common mistake I make is forgetting
commas.  This results in a file that wont compile.

If you get something like;

    TypeError at /some-root/999/some-page

    'tuple' object is not callable

Then you forgot a comma after a tuple.

If you get an error complaining about something being an invalid index
then you forgot a comma after a list.  Eg

    (body,
     (h1, "Some title"),
     (ul,
      [(li, "dynamic content: ", idx) for idx in range(10)]     <-- need a comma here
      (li, "some custom footer li")))

If you are a lisper then you will probably make this mistake all the
time (well I do anyway) but it is quickly corrected and as a benefit
you get to navigate around the structure using all those emac's
keybindings that are burned into your brain.

## Official Releases

None, everything could change at anytime!  Use at your risk.

If you do use this library please let me know how you think it could
be improved.

## Footnotes

<strong>i.</strong> Django claims that non-technical users can use
their templating system and that this frees the developers from having
to worry about the presentation layer.  Their use case is quite
specific (newspaper publishing) but personally I've never had any
success with integrating non-developers into the software process in
this way.

In my experience the restrictions and conventions required to make
such a practice work are far worse then just dedicating a portion of
time to converting mock ups to code and keeping them updated.

Your mileage may vary.

<strong>ii.</strong> A simple renderer_p decorator is provided for
this purpose.

<strong>iii.</strong> utils.py provides an attrs function that has the
following useful features for producing a dictionary tailored for
generating attributes.

* The key of 'classes' is _special_.

  It will be emitted as 'class'.

  It can be a string or a list.

  Lists elements are joined with a single space in preparation for
  output.

* Double underscores in attribute names are converted to colons,
  provding poor man's namespace support.

* The first parameter to attrs can specify an 'id' and classes.

  This is similar to what HAML does.  For example;

    "#id class1 class2" becomes id="id" class="class1 class2"

    "classA classB classC" becomes class="class1 class2"

  See the examples for usage.
