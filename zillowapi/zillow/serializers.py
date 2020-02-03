from rest_framework import serializers

from .models import Zillow


class ZillowDetailSerializer(serializers.ModelSerializer):
  """The Zillow Object Serializer"""

  class Meta:
    model = Zillow
    fields = '__all__'
    read_only_fields = ("id",)
