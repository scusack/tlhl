from types import ListType, TupleType, StringTypes, DictType

# --------------------------------------------------------------------------------
# Utils and shortcuts

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
