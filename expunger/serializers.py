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


class AttorneySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Attorney
        fields = ["url", "pk", "bar", "name"]
        extra_kwargs = {"url": {"view_name": "expunger:attorney-detail"}}

    name = serializers.SerializerMethodField("attorney_name")

    def attorney_name(self, attorney):
        return "%s %s" % (attorney.user.first_name, attorney.user.last_name)
