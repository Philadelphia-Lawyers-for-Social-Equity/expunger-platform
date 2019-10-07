from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers


class AddressView(APIView):
    """
    View to show an individual address via the JSON API
    """
    def get(self, request, pk, *args, **kwargs):
        """
        Produce the address via id
        """
        address = get_object_or_404(models.Address, pk=pk)
        serializer = serializers.AddressSerializer(
            address, context={"request": request})

        return Response(serializer.data)
