from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)
    # .get is a function which will get a value and return appropriate value