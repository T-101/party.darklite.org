from django.utils import timezone
from typing import Union


def _do_date_parse(date_str: Union[str, None]) -> timezone.datetime.date:
    try:
        return timezone.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z").date()
    except (ValueError, TypeError):
        return timezone.datetime.strptime("1970-01-01T00:00:00+02:00", "%Y-%m-%dT%H:%M:%S%z").date()


# Payload is the json response from the demoparty.net API converted to a dictionary

def get_start_date(payload: dict) -> timezone.datetime.date:
    date_str = payload.get("startDate")
    return _do_date_parse(date_str)


def get_end_date(payload: dict) -> timezone.datetime.date:
    date_str = payload.get("endDate")
    return _do_date_parse(date_str)


def get_location(payload: dict) -> str:
    address = []
    location = payload.get("location", {})

    if location:
        if location.get("@type") == "VirtualLocation":
            location_str = "Online"
        else:
            street_address = location.get("address", {}).get("streetAddress", "")
            if street_address:
                address.append(street_address)
            postal_code = location.get("address", {}).get("postalCode", "")
            if postal_code:
                address.append(postal_code)
            address_locality = location.get("address", {}).get("addressLocality", "")
            if address_locality:
                address.append(address_locality)
            location_str = ", ".join([p for p in address if p != ""])

    else:
        location_str = "Unknown"
    return location_str


def get_country(payload: dict) -> str:
    location = payload.get("location", {})
    if location:
        location_str = location.get("address", {}).get("addressCountry", "")
        if type(location_str) is str:
            location_str = location_str[-2:]
    else:
        location_str = payload.get("locationCountry", "")
        if type(location_str) is str:
            location_str = location_str[-2:]
    return location_str
