# -*- coding: utf-8 -*-

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

from django.middleware.csrf import get_token
from django.forms import FileField

def set_model_info(model, fields):
    object_name  = model._meta.object_name
    verbose_name = model._meta.verbose_name
    for field in fields :
        field.model_name         = object_name
        field.model_verbose_name = verbose_name
    return fields

def get_form_fields(form):
    # FIXME: should cache already computed makers
    fields = [f for f in form]
    if hasattr(form, 'instance'):
        set_model_info(form.instance, fields)
    maker = namedtuple("FormTuple", [f.name for f in fields])
    return maker._make(fields)

def get_model_fields(model):
    fields = set_model_info(model, [f for f in model._meta.fields])
    maker = namedtuple("ModelTuple", [f.name for f in fields])
    return maker._make(fields)

def field_value(field):
    """
    Returns the value of the field from the initial data of the form
    when appropriate or from the form.

    This has been pulled from the BoundField.as_widget method.
    """
    if not field.form.is_bound:
        data = field.form.initial.get(field.name, field.field.initial)
        return callable(data) and data() or data

    if isinstance(field.field, FileField) and field.data is None:
        return field.form.initial.get(field.name, field.field.initial)

    return field.data

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

@django_field_renderer
def as_hidden(field, printer):
    printer.raw(field.as_hidden())

@renderer
def value(params, printer):
    model, field = canonicalise_params(params, attrs=False, length=2)
    display_name = "get_{0}_display".format(field.name)
    if hasattr(model, display_name):
        return getattr(model, display_name)()
    return getattr(model, field.name, "")

@renderer
def csrf_token(params, printer):
    attrs, request = canonicalise_params(params, length=1)
    attrs.update(dict(name='csrfmiddlewaretoken',
                      value=get_token(request)))
    return (hidden, attrs)
