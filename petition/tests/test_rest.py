# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from expunger.tests.test_rest import Authenticated
from petition import factories


class TestRest(Authenticated, TestCase):
    """Make sure the REST interface works"""

    def test_petition(self):
        """Petitions can be produced via REST"""
        petitioner = factories.PetitionerFactory()
        docket = factories.DocketIdFactory()
        petition = factories.PetitionFactory()
        restitution = factories.RestitutionFactory()

        data = {
            "petitioner": {
                "name": petitioner.name,
                "aliases": petitioner.aliases,
                "dob": petitioner.dob.isoformat(),
                "ssn": petitioner.ssn,
                "address": {
                    "street1": petitioner.address.street1,
                    "street2": petitioner.address.street2,
                    "city": petitioner.address.city,
                    "state": petitioner.address.state,
                    "zipcode": petitioner.address.zipcode
                }
            },
            "petition": {
                "date": petition.date,
                "petition_type": petition.petition_type.name,
                "otn": petition.otn,
                "dc": petition.dc,
                "arrest_date": petition.arrest_date.isoformat(),
                "arrest_officer": petition.arrest_officer,
                "disposition": petition.disposition,
                "judge": petition.judge,
            },
            "docket": str(docket),
            "restitution": {
                "total": restitution.total,
                "paid": restitution.paid
            }
        }

        url = reverse("petition:generate")
        res = self.authenticated_client.post(url, data, content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_post_docket(self):
        """Possible to post a docket file."""
        url = reverse("petition:parse-docket")
        f = SimpleUploadedFile("MC-51-CR-0000076-2019.pdf", b"content")
        res = self.authenticated_client.post(url, {"docket_file": f})
        self.assertEqual(res.status_code, 200)
