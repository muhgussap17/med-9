from django import template
from core.utils.hashid import encode_id

register = template.Library()

@register.filter
def encode_hash(value):
    return encode_id(value)
