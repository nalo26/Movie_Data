from django import template

register = template.Library()


@register.simple_tag
def get_poster_url(uri):
    return f"https://www.themoviedb.org/t/p/w1280{uri}"
