import os
import json

from django.test import TestCase
from django.conf import settings

from party.parsers import get_location, get_country, get_start_date, get_end_date


class ParserTest(TestCase):
    def setUp(self):
        files = ["inercia2023.json", "birdie2024.json"]
        self.payloads = []
        for file in files:
            filepath = os.path.join(settings.BASE_DIR, "party/tests", file)
            with open(filepath, "r") as f:
                self.payloads.append(json.load(f))

    def test_location_parser(self):
        self.assertEqual(get_location(self.payloads[0]), "Unknown")

        self.assertEqual(get_location(self.payloads[1]), "Uppsala, Sweden, Uppsala")

    def test_country_parser(self):
        self.assertEqual(get_country(self.payloads[0]), "PT")
        self.payloads[0]["location"] = None
        self.assertEqual(get_country(self.payloads[0]), "PT")
        self.payloads[0]["locationCountry"] = None
        self.assertIsNone(get_country(self.payloads[0]))

        self.assertEqual(get_country(self.payloads[1]), "SE")

    def test_date_parser(self):
        self.assertEqual(get_start_date(self.payloads[0]).strftime("%Y-%m-%d"), "2023-12-01")
        self.assertEqual(get_end_date(self.payloads[0]).strftime("%Y-%m-%d"), "2023-12-03")
        self.payloads[0]["startDate"] = None
        self.assertEqual(get_start_date(self.payloads[0]).strftime("%Y-%m-%d"), "1970-01-01")

        self.assertEqual(get_start_date(self.payloads[1]).strftime("%Y-%m-%d"), "2024-05-09")
        self.assertEqual(get_end_date(self.payloads[1]).strftime("%Y-%m-%d"), "2024-05-12")
        self.payloads[0]["endDate"] = None
        self.assertEqual(get_end_date(self.payloads[0]).strftime("%Y-%m-%d"), "1970-01-01")
