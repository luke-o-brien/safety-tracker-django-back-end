from .common import AuthorSerializer
from stories.serializers.common import StorySerializer

class PopulatedAuthorSerializer(AuthorSerializer):
    stories = StorySerializer(many=True)

