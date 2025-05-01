from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from party.models import Party, Trip


class URLS:
    create_party = reverse("party:create")


def get_credentials(user_type):
    return {"password": "123", "email": f"{user_type}@example.com"}


class ViewTests(TestCase):
    fixtures = ["party/tests/test_users.json"]

    test_party = {
        "name": "Test Party",
        "location": "Test Location",
        "date_start": "2023-12-01",
        "date_end": "2023-12-03",
        "country": "FI",
        "www": "https://example.com",
    }

    test_trip = {
        "display_name": "Test User",
        "type": "plane",
        "departure_town": "CityTown",
        "departure_country": "FI",
        "departure_datetime": "2023-12-01 12:34",
        "arrival_town": "PartyTown",
        "arrival_country": "FI",
        "arrival_datetime": "2023-12-01 14:56",
    }

    def test_create_party(self):
        self.client.login(**get_credentials("normal"))
        response = self.client.get(URLS.create_party)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(URLS.create_party, data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        response = self.client.post(URLS.create_party, data=self.test_party)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertEqual(Party.objects.count(), 1)
        party = Party.objects.get(pk=1)
        response = self.client.get(reverse("party:detail", args=[party.slug]))
        self.assertEqual(response.status_code, 200)

    def test_create_party_trip(self):
        self.client.login(**get_credentials("normal"))
        self.client.post(URLS.create_party, data=self.test_party)
        self.assertEqual(Party.objects.count(), 1)
        party = Party.objects.get(pk=1)
        self.assertEqual(party.name, "Test Party")
        self.assertEqual(party.slug, "test-party-2023")
        response = self.client.get(reverse("party:detail", args=[party.slug]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("party:create-trip-to", args=[party.slug]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertTrue(str(messages[0]).startswith("Cannot create a trip to a party that has ended"))

        party.date_end = timezone.now() + timezone.timedelta(days=3)
        party.save()
        response = self.client.get(reverse("party:create-trip-to", args=[party.slug]))
        self.assertEqual(response.status_code, 200)
        payload = self.test_trip
        payload["party"] = party
        response = self.client.post(reverse("party:create-trip-to", args=[party.slug]), data=payload)
        self.assertRedirects(response, reverse("party:detail", args=[party.slug]), status_code=302,
                             target_status_code=200)
        self.assertEqual(Trip.objects.count(), 1)
