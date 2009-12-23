from types import DictType

# --------------------------------------------------------------------------------
# Elements

class Element(object):
    def __init__(self, tag_name, block_p, explicit_end_p, attrs=None):
        self.tag_name       = tag_name
        self.block_p        = block_p
        self.explicit_end_p = explicit_end_p
        self.attrs          = attrs or {}

def make_block(tag_name, attrs=None, explicit_end_p=False):
    return Element(tag_name, True, explicit_end_p, attrs)

def make_inline(tag_name, attrs=None, explicit_end_p=False):
    return Element(tag_name, False, explicit_end_p, attrs)


# --------------------------------------------------------------------------------
# Renderers


def renderer(func):
    "Simple decorator to turn a function into a tag renderer."

    func.renderer_p = True
    return func

def renderer_p(thing):
    return getattr(thing, 'renderer_p', False)

@renderer
def raw(contents, printer):
    map(printer.raw, contents)

@renderer
def cdata(contents, printer):
    printer.raw('\n// <![CDATA[')
    map(printer.raw, contents)
    printer.raw('// ]]>\n')
