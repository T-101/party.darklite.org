from django.test import TestCase
from django.urls import reverse


class URLS:
    landing_page = reverse("party:landing_page")
    party_list = reverse("party:list")
    party_list_by_year = reverse("party:list-by-year", args=[2025])
    party_list_by_country = reverse("party:list-by-country", args=["Finland"])
    party_list_by_country_and_year = reverse("party:list-by-country-and-year", args=["Finland", 2025])
    about = reverse("party:about")
    stats = reverse("party:stats")
    profile = reverse("authentication:profile")
    create_party = reverse("party:create")


def get_credentials(user_type):
    return {"password": "123", "email": f"{user_type}@example.com"}


class ViewTests(TestCase):
    fixtures = ["party/tests/test_users.json"]

    def test_public_views(self):
        response = self.client.get(URLS.landing_page)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.party_list)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.party_list_by_year)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.party_list_by_country)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.party_list_by_country_and_year)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.about)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("feeds"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("feeds-rss2"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("feeds-rss09"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("feeds-atom1"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_views_as_anonymous(self):
        response = self.client.get(URLS.stats)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(URLS.stats, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        response = self.client.get(URLS.profile)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(URLS.create_party)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_views_as_normal_user(self):
        response = self.client.get(URLS.stats)
        self.assertEqual(response.status_code, 302)

        self.client.login(**get_credentials("normal"))

        response = self.client.get(URLS.stats)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.profile)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(URLS.create_party)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(URLS.stats)
        self.assertEqual(response.status_code, 302)
