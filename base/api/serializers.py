# classes that take a python model or object and turn it into JSON to return from API

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
  class Meta:
    model = Room
    fields = '__all__'