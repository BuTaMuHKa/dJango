from django import template

register = template.Library()

@register.filter
def currency(value, name='руб.'):
    return '%1.2f %s' % (value, name)

register.filter('currency', currency)

@register.simple_tag
def lst(sep, *args):
    return '%s (итог %s)' % (sep.join(args), len(args))
