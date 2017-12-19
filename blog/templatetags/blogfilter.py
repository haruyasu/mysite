import html.parser
import re
from django import template
from django.template.defaultfilters import urlize
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData

register = template.Library()
html_parser = html.parser.HTMLParser()

def url(text):
    text = text.replace('<br />', '\n')
    text = text.replace('[filter url]', '').replace('[end]', '')
    tag = urlize(text)
    tag = tag.replace('<a ', '<a target="_blank" rel="nofollow" ')
    return tag

def html(text):
    text = text.replace('<br />', '\n')
    text = text.replace('[filter html]', '').replace('[end]', '')
    tag = html_parser.unescape(text)
    return tag

def img(text):
    text = text.replace('<br />', '\n')
    text = text.replace('[filter img]', '').replace('[end]', '')
    tag = (
        '<a href="{0}" target="_blank" rel="nofollow"><img src="{0}" '
        'class="img-fluid"/></a>'
    ).format(text)
    return tag

def cord(text):
    text = text.replace('<br />', '\n')
    text = text.replace('[filter cord]', '').replace('[end]', '')
    tag = '<pre class="prettyprint linenums">{}</pre>'.format(text)
    return tag

def quote(text):
    text = text.replace('[filter quote]', '').replace('[end]', '')
    tag = '<blockquote class="blockquote"><p>{}</p></blockquote>'.format(
        text)
    return tag

def midasi1(text):
    text = text.replace('[filter midasi1]', '').replace('[end]', '')
    tag = '<p class="midasi1">{0}</p>'.format(text)
    return tag

@register.filter(is_safe=True, needs_autoescape=True)
def blog(value, autoescape=True):
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)
    filters = re.finditer(r'\[filter (?P<tag_name>.*?)\].*?\[end\]', value)
    results = []
    for f in filters:
        filter_name = f.group('tag_name')
        origin_text = f.group()
        filter_function = globals().get(filter_name)
        if filter_function and callable(filter_function):
            result_text = filter_function(origin_text)
        else:
            result_text = origin_text
        results.append((origin_text, result_text))

    for origin_text, result_text in results:
        if origin_text != result_text:
            value = value.replace(origin_text, result_text)
    return mark_safe(value)

@register.simple_tag
def url_replace(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()

@register.simple_tag
def hilight(text, key_word):
    result = text
    case = (key_word, key_word.title(), key_word.capitalize())
    for word in case:
        html_tag = '<span class="under-line">{0}</span>'.format(word)
        result = result.replace(word, html_tag)
    return result

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
