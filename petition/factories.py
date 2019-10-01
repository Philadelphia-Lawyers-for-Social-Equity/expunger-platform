# -*- coding: utf -*-
from datetime import date
import factory
import factory.fuzzy
from .models import Address, Petitioner, Court, CaseType, DocketId, \
    PetitionType, Petition, Restitution


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    street1 = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zipcode = factory.Faker("zipcode")


class PetitionerFactory(factory.Factory):
    class Meta:
        model = Petitioner

    name = factory.Faker("name")
    aliases = []
    dob = factory.Faker("date_this_century")
    ssn = factory.Faker("ssn")
    address = factory.SubFactory(AddressFactory)


class DocketIdFactory(factory.Factory):
    class Meta:
        model = DocketId

    court = factory.fuzzy.FuzzyChoice(Court)
    case_type = factory.fuzzy.FuzzyChoice(CaseType)
    number = factory.fuzzy.FuzzyInteger(1, 9999999)
    year = factory.fuzzy.FuzzyInteger(1968, 2019)


class PetitionFactory(factory.Factory):
    class Meta:
        model = Petition

    date = date.today()
    petition_type = factory.fuzzy.FuzzyChoice(PetitionType)
    otn = factory.fuzzy.FuzzyInteger(1000000, 9999999)
    dc = factory.fuzzy.FuzzyInteger(1000000000, 9999999999)
    arrest_date = factory.Faker("date_this_century")
    arrest_officer = factory.Faker("name")
    disposition = "dismissed"
    judge = factory.Faker("name")


class RestitutionFactory(factory.Factory):
    class Meta:
        model = Restitution

    total = factory.fuzzy.FuzzyInteger(500, 1000)
    paid = factory.fuzzy.FuzzyInteger(0, 499)
