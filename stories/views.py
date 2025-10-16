from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Story
from .serializers import StorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly # IsAuthenticatedOrReadOnly specifies that a view is secure on all methods except get requests


# Creating views here

class StoryListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, ) # sets the permission levels of the specific view by passing in the rest framework authentication class
    # handle a GET request in the StoryListView
    def get(self, _request):
        # go to the database and get all the stories
        stories = Story.objects.all()
        # translate the stories from the database to a usable form
        serialized_stories = StorySerializer(stories, many=True)
        # return the serialized data and a 200 status code
        return Response(serialized_stories.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["owner"] = request.user.id
        story_to_add = StorySerializer(data=request.data)
        try:
           story_to_add.is_valid()
           story_to_add.save()
           return Response(story_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

   