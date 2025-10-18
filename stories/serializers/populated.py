from .common import StorySerializer
from authors.serializers.common import AuthorSerializer
from authentication.serializers import UserSerializer
from comments.serializers.populated import PopulatedCommentSerializer

class PopulatedStorySerializer(StorySerializer):
    author = AuthorSerializer()
    owner = UserSerializer()
    comments = PopulatedCommentSerializer(many=True)
    
# Populated comments working on Postman