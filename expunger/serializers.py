from rest_framework import serializers
from . import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ["pk", "street1", "street2", "city", "state",
                  "zipcode"]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization
        fields = ["url", "pk", "name", "phone", "address", "address"]
        extra_kwargs = {"url": {"view_name": "expunger:organization-detail"}}

    address = AddressSerializer()
