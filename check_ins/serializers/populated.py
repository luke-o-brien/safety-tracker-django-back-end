from .common import Check_InSerializer
from authentication.serializers import UserSerializer

class PopulatedCheck_InSerializer(Check_InSerializer):
    owner = UserSerializer()

