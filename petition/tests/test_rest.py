# -*- coding: utf-8 -*-

from pathlib import Path

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
                "arrest_agency": petition.arrest_agency,
                "arrest_date": petition.arrest_date.isoformat(),
                "arrest_officer": petition.arrest_officer,
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

        pdf2 = Path(__file__).parent / "data" / "test-02.pdf"

        with pdf2.open("rb") as f:
            res = self.authenticated_client.post(url, {"docket_file": f})

        self.assertEqual(res.status_code, 200)
        jsr = res.json()

        self.assertEqual(
            jsr["petitioner"],
            {
                "name": "Michael Jackson",
                "aliases": None,
                "dob": "1966-03-17"
            }
        )

        self.assertEqual(
            jsr["petition"],
            {
                "arrest_agency": "Philadelphia Pd",
                "arrest_date": "1984-12-23",
                "arrest_officer": "Affiant",
                "judge": "O'Keefe, Joseph D.",
                "otn": "M 212189-5",
            }
        )

        self.assertEqual(jsr["docket"], "CP-51-CR-0201031-1985")

        self.assertEqual(
            jsr["charges"],
            [
                {
                    "description": "THEFT BY UNLAWFUL TAKING OR DISPOSITION",
                    "statute": "18 § 3921",
                    "date": "1985-04-29",
                    "grade": None,
                    "disposition": "Nolle Prossed"
                },
                {
                    "description": "THEFT BY RECEIVING STOLEN PROPERTY",
                    "statute": "18 § 3925",
                    "date": "1985-04-29",
                    "grade": None,
                    "disposition": "Nolle Prossed"
                },
                {
                    "description": "CRIMINAL CONSPIRACY",
                    "statute": "18 § 903",
                    "date": "1985-04-29",
                    "grade": None,
                    "disposition": "Nolle Prossed"
                },
                {
                    "description": "ROBBERY",
                    "statute": "18 § 3701",
                    "date": "1985-04-29",
                    "grade": None,
                    "disposition": "Nolle Prossed"
                }
            ]
        )
        self.assertEqual(jsr["restitution"], {"total": None, "paid": None})
