import markdown
from django import template
from datetime import datetime
from django.utils.safestring import mark_safe

register = template.Library()


# https://python-markdown.github.io/extensions/
@register.filter()
def mark(value):
    '''
    apply markdown for post content
    '''
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

