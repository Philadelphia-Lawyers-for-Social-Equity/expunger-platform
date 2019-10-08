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
        cls.authenticated_client = client


class TestRest(Authenticated, TestCase):
    """Test the JSON API"""

    def test_read_organization(self):
        """ """
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
