from django import template

register = template.Library()


@register.filter
def split(value, key):
    """
    Splits the string by the given key and returns a list.
    """
    if value:
        return value.split(key)
    return []
