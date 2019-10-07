from rest_framework import serializers
from . import models


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Address
        fields = ["url", "pk", "street1", "street2", "city", "state",
                  "zipcode"]
        extra_kwargs = {"url": {"view_name": "expunger:address-detail"}}
