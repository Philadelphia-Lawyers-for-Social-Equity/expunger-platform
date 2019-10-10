# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.urls import reverse

from expunger import factories


class Authenticated:
    """Provide an authenticated client for Tests"""

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        pw = factories.random_text(8)
        profile = factories.ExpungerProfileFactory()
        profile.user.set_password(pw)
        profile.user.save()

        client = Client()
        success = client.login(username=profile.user.username, password=pw)
        if not success:
            raise RuntimeError("Failed to produce authenticated client")

        cls.authenticated_profile = profile
        cls.authenticated_client = client


class TestRest(Authenticated, TestCase):
    """Test the JSON API"""

    def test_read_organization(self):
        """API shows a single organization"""
        org = factories.OrganizationFactory()
        org.refresh_from_db()
        url = reverse("expunger:organization-detail", kwargs={"pk": org.pk})
        res = self.authenticated_client.get(url)
        jsr = res.json()

        self.assertEqual(jsr["name"], org.name)
        self.assertEqual(jsr["phone"], org.phone)
        self.assertEqual(jsr["address"]["street1"], org.address.street1)
        self.assertEqual(jsr["address"]["city"], org.address.city)
        self.assertEqual(jsr["address"]["state"], org.address.state)
        self.assertEqual(jsr["address"]["zipcode"], org.address.zipcode)

    def test_read_attorney(self):
        """API shows a single attortey"""
        attorney = factories.AttorneyFactory()
        attorney.refresh_from_db()
        url = reverse("expunger:attorney-detail", kwargs={"pk": attorney.pk})
        res = self.authenticated_client.get(url)
        jsr = res.json()

        self.assertEqual(jsr["name"], "%s %s" % (
            attorney.user.first_name, attorney.user.last_name))
        self.assertEqual(jsr["bar"], attorney.bar)

    def test_my_profile(self):
        """API allows user to review their own profile"""
        url = reverse("expunger:profile")
        res = self.authenticated_client.get(url)
        jsr = res.json()

        self.assertEqual(jsr["user"]["first_name"],
                         self.authenticated_profile.user.first_name)
        self.assertEqual(jsr["user"]["last_name"],
                         self.authenticated_profile.user.last_name)
        self.assertEqual(jsr["user"]["username"],
                         self.authenticated_profile.user.username)
        self.assertEqual(jsr["user"]["email"],
                         self.authenticated_profile.user.email)

        self.assertEqual(jsr["attorney"]["pk"],
                         self.authenticated_profile.attorney.pk)
        self.assertEqual(jsr["organization"]["pk"],
                         self.authenticated_profile.organization.pk)
