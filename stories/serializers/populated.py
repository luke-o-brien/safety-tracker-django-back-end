from .common import StorySerializer
from authors.serializers.common import AuthorSerializer
from authentication.serializers import UserSerializer

class PopulatedStorySerializer(StorySerializer):
    author = AuthorSerializer()
    owner = UserSerializer()
    