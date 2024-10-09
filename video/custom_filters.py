from django import template

register = template.Library()

@register.filter
def replace_extension(value, arg):
    """Replaces the file extension with the provided argument."""
    return value.replace('.srt', arg)
