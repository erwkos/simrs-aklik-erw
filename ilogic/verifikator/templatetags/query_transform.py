# your_app/templatetags/query_transform.py

from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """
    Mengubah atau menambahkan parameter query.
    Contoh penggunaan: {% query_transform request page=2 %}
    """
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()
