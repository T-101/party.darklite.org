import re

from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from django_countries import countries


@register.filter
def get_destination_text(s):
    if type(s) == str:
        return re.sub(COUNTRY_CODE_REGEX, r'\1', s, re.IGNORECASE)
    return s.iata_code


@register.filter
def get_destination_country(s):
    if type(s) == str:
        return re.sub(COUNTRY_CODE_REGEX, r'\2', s.lower(), re.IGNORECASE)
    return s.country.lower()


COUNTRY_CODES = [x.lower() for x in countries.countries]
COUNTRY_CODE_REGEX = r'(.*),\s(%s)$' % '|'.join(COUNTRY_CODES)


@register.filter
def get_display_name(obj):
    if obj.display_name:
        return obj.display_name
    return obj


@register.filter
def small_year(obj):
    return mark_safe(f"{obj.name} <small>{obj.date_start.year}</small>")
