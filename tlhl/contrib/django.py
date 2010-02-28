"""

Most of the work is already done as Django uses __unicode__ for a most of
the wiget to html conversion.

This module provides mainly provides wrappers to emit the django widgets in
a 'raw' renderer.

"""

from collections import namedtuple
from functools import wraps, partial

import tlhl
from tlhl.utils import attrs, canonicalise_params
from tlhl.xhtml10 import *


def get_bound_fields(form):
    # FIXME: should cache already computed makers

    bound_fields = [f for f in form]
    maker = namedtuple("FormTuple", [f.name for f in bound_fields])
    return maker._make(bound_fields)

def django_field_renderer(func):
    @wraps(func)
    @renderer
    def field_renderer(params, printer):
        attrs, field = canonicalise_params(params, length=1)
        if attrs : field.as_widget = partial(field.as_widget, attrs=attrs)
        return func(field, printer)

    return field_renderer

def django_form_renderer(func):
    @wraps(func)
    @renderer
    def form_renderer(params, printer):
        form = canonicalise_params(params, attrs=False, length=1)
        return func(form, printer)

    return form_renderer

@django_form_renderer
def management_form(formset, printer):
    printer.raw(unicode(formset.management_form))

@django_form_renderer
def non_field_errors(form, printer):
    printer.raw(unicode(form.non_field_errors()))

@django_field_renderer
def help(field, printer):
    if field.help_text :
        return (div, attrs("help-text"), field.help_text)

@django_field_renderer
def errors(field, printer):
    if field.errors :
        return (ul, attrs("errorlist"),
                [(li, error) for error in field.errors])

@django_field_renderer
def label(field, printer):
    printer.raw(unicode(field.label_tag()))

@django_field_renderer
def widget(field, printer):
    printer.raw(unicode(field))

@django_field_renderer
def field(field, printer):
    return [(widget, field),
            (help,   field),
            (errors, field)]
