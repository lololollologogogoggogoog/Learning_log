from django import template
from django.http import Http404

from library.tools import Protection

register = template.Library()

@register.simple_tag()
def gen_error():
    raise Http404
