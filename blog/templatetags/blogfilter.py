import html.parser
from django import template
from django.utils import timezone
from django.template.defaultfilters import stringfilter
import markdown

register = template.Library()
html_parser = html.parser.HTMLParser()

@register.simple_tag
def url_replace(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()

@register.simple_tag
def by_the_time(dt):
    result = timezone.now() - dt
    s = result.total_seconds()
    hours = int(s / 3600)
    if hours >= 24:
        day = int(hours / 24)
        return '{0} days ago'.format(day)
    elif hours == 0:
        minute = int(s / 60)
        return '{0} minutes ago'.format(minute)
    else:
        return '{0} hours ago'.format(hours)

@register.filter
@stringfilter
def markdown2html(value):
    return markdown.markdown(value, ['fenced_code'])

@register.filter
@stringfilter
def markdown2post(value):
    s = value.replace("#", "")
    s = s.replace("*", "")
    s = s.replace("```", "")
    s = s[:140]
    s = s + "..."
    return s