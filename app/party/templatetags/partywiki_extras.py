import re

from django.template.defaulttags import register
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
