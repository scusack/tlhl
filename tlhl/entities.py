from base import raw

def make_entity(name):
    return (raw, "&{0};".format(name))

NBSP   = make_entity('nbsp')
RSAQUO = make_entity('rsaquo')
BRVBAR = make_entity('brvbar')
LARR   = make_entity('larr')
UARR   = make_entity('uarr')
RARR   = make_entity('rarr')
DARR   = make_entity('darr')
DIAMS  = make_entity('diams')
