import html.parser
from django import template

register = template.Library()
html_parser = html.parser.HTMLParser()

@register.simple_tag
def url_replace(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()
