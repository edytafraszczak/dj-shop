from django import template

register = template.Library()


@register.filter(name='flag')
def flag(country_code):
    if country_code.lower() == "en":
        return "gb"
    else:
        return country_code
