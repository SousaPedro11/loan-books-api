def get_fields_tuple(model):
    t = []
    if model._meta:
        t = list((_.name, _.name) for _ in model._meta.fields)
    return t
