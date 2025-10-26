# We need a serializer to convert python objects into JSON
from rest_framework import serializers
from ..models import Check_In

class Check_InSerializer(serializers.ModelSerializer):
  class Meta:
    model = Check_In
    # This part below converts all fields from json to sql.
    fields = ['title', 'description', 'day_type', 'relaxed_today', 'category', 'reaction_level', 'coping_action', 'effectiveness']

