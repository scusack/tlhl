from types import DictType
from utils import flatten

# --------------------------------------------------------------------------------
# Elements

class Element(object):
    def __init__(self, tag_name, block_p, explicit_end_p, has_content_p, attrs=None):
        self.tag_name       = tag_name
        self.block_p        = block_p
        self.explicit_end_p = explicit_end_p
        self.has_content_p  = has_content_p
        self.attrs          = attrs or {}

def make_block(tag_name, attrs=None, explicit_end_p=False, has_content_p=True):
    return Element(tag_name, True, explicit_end_p, has_content_p, attrs=attrs)

def make_inline(tag_name, attrs=None, explicit_end_p=False, has_content_p=True):
    return Element(tag_name, False, explicit_end_p, has_content_p, attrs=attrs)

# --------------------------------------------------------------------------------
# Renderers

def renderer(func):
    "Simple decorator to turn a function into a tag renderer."

    func.renderer_p = True
    return func

def renderer_p(thing):
    return getattr(thing, 'renderer_p', False)

@renderer
def raw(params, printer):
    for param in flatten(params):
        printer.raw(unicode(param))
