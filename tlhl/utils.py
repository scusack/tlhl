from types import ListType, TupleType, StringTypes, DictType

# --------------------------------------------------------------------------------
# Utils and shortcuts
#
def attrs(identity=None, classes=None, **kwargs):
    """
    Mimics the id/class generation of toolkits like HAML, etc.

    Turns __ in kwarg keys into : for a poor mans namespace support.
    """
    result      = {}
    class_names = []

    if identity :
        # identity spec ala HAML, etal.
        if identity.startswith('#') :
            components = identity.split(' ')
            result['id'] = components[0][1:]
            class_names.extend(components[1:])
        else :
            class_names.append(identity.strip())

    if isinstance(classes, (ListType, TupleType)):
        class_names.extend([c.strip() for c in filter(None, classes)])

    elif isinstance(classes, StringTypes):
        class_names.append(classes)

    if class_names:
        result['class'] = ' '.join(class_names)

    for key, value in kwargs.items() :
        key = key.replace('__', ':')
        result[key] = value

    return result

def canonicalise_params(params, attrs=None, length=None):
    """
    Convenience function for handling the common case where you are called with;

    (some-element, attrs-dict, param1, param2, ...)

    and you want to set ups some defaults for the attrs-dict, then
    override it with attrs-dict but also handle the case where there
    are no overrides.
    """
    final_attrs = {}
    if params and isinstance(params[0], DictType):
        final_attrs = params[0]
        params = params[1:]

    if attrs is False and final_attrs :
        raise Exception("Unexpected attributes found, {0}".format(final_attrs))

    if length and len(params) != length:
        raise Exception("Invalid number of params, expected {0}, got {1}".format(length,
                                                                                 len(params)))

    if attrs :
        [final_attrs.setdefault(key, value) for key, value in attrs.items()]

    if length == 1:
        params = params[0]

    if attrs is False: return params

    return final_attrs, params

# --------------------------------------------------------------------------------
# Efficient list flattening
#
def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)
