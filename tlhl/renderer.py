"""
Need to move a bunch of the html tag elements into a dialect and base it on this;

http://xhtml.com/en/xhtml/reference/
"""
from xml.sax.saxutils import quoteattr, escape
from types import *
from cStringIO import StringIO
from base import renderer_p, Element

class PrettyPrinter(object):
    def __init__(self):
        self.stream  = StringIO()
        self.indent_ = -1

    def show(self):
        return self.stream.getvalue()

    def raw(self, value):
        """
        Escape hatch to pump whatever it is straight to the printer.
        """
        self.stream.write(value)

    def get_output(self):
        return self.stream.getvalue()

    def indent(self):
        self.indent_ += 1

    def undent(self):
        self.indent_ -= 1

    def new_line(self, indent_p=True):
        self.stream.write("\n")
        if indent_p and self.indent_:
            self.stream.write("  " * self.indent_)

    def open_start_tag(self, tag_name):
        self.stream.write(u"<")
        self.stream.write(unicode(tag_name))

    def close_start_tag(self):
        self.stream.write(u">")

    def close_tag(self, tag_name, explicit_p, start_tag_open_p=True):
        if start_tag_open_p :
            if explicit_p :
                self.stream.write(u">")
                self.stream.write(u"</")
                self.stream.write(unicode(tag_name))
                self.stream.write(u">")
            else:
                self.stream.write(u" />")
        else:
            self.stream.write(u"</")
            self.stream.write(unicode(tag_name))
            self.stream.write(u">")

    def text(self, value):
        self.stream.write(escape(value))

    def attribute(self, name, value):
        if value is False or value is None : return

        # standard way of representing truth in x/html, ie checked="checked" or checked=""
        if value is True :
            value = name

        self.stream.write(" ")
        self.stream.write(unicode(name))
        self.stream.write('=')
        self.stream.write(quoteattr(unicode(value)))

def render(exp, printer):
    if exp is None or exp is False: return

    if isinstance(exp, TupleType):
        if not exp : return
        render_expression(exp, printer)

    elif isinstance(exp, ListType):
        if not exp : return
        [render(e, printer) for e in exp]

    else:
        # Some sort of scalar, let it turn itself into unicode and jam
        # it into the printer.
        printer.text(unicode(exp))

    return printer

# --------------------------------------------------------------------------------

def render_expression(exp, printer):
    if renderer_p(exp[0]) :
        # call the renderer giving it the printer so it can do
        # whatever it want to the stream and also call render on the
        # result of the call so that it can just give us some 'valid'
        # TLHL to render.
        render(exp[0](exp[1:], printer),
               printer)
        return

    elem, attrs, contents = canonicalise_exp(exp)

    if elem.block_p :
        printer.indent()
        printer.new_line()

    printer.open_start_tag(elem.tag_name)
    if attrs :
        for name, value in attrs.iteritems():
            printer.attribute(name, value)

    if elem.attrs:
        for name, value in elem.attrs.iteritems():
            # skip ones already emitted
            if attrs and attrs.has_key(name): continue
            printer.attribute(name, value)

    if contents :
        printer.close_start_tag()
        render(contents, printer)
        printer.close_tag(elem.tag_name, elem.explicit_end_p, start_tag_open_p=False)
    else :
        printer.close_tag(elem.tag_name, elem.explicit_end_p, start_tag_open_p=True)

    if elem.block_p:
        printer.undent()

def canonicalise_exp(exp):
    """
    Returns elem, attributes, contents
    """
    elem     = exp[0]
    attrs    = None
    contents = None

    if len(exp) > 1:
        if isinstance(exp[1], DictType):
            attrs    = exp[1]
            contents = list(exp[2:])
        else :
            contents = list(exp[1:])

    return elem, attrs, contents
