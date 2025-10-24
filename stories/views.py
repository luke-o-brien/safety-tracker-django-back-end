from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Story
from .serializers.common import StorySerializer
from .serializers.populated import PopulatedStorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly # IsAuthenticatedOrReadOnly specifies that a view is secure on all methods except get requests


# Creating views:

class StoryListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, ) # sets the permission levels of the specific view by passing in the rest framework authentication class
    # handle a GET request in the StoryListView
    # Get all stories
    def get(self, _request):
        # go to the database and get all the stories
        stories = Story.objects.all()
        # translate the stories from the database to a usable form
        serialized_stories = PopulatedStorySerializer(stories, many=True)
        # return the serialized data and a 200 status code
        return Response(serialized_stories.data, status=status.HTTP_200_OK)
    
    # Create a story with post method
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


class StoryDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, ) # sets the permission levels of the specific view by passing in the rest framework authentication class

    # Retrieving a single story from the database and error if it's not found
    def get_story(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise NotFound(detail="Can't find that story!") # <-- imported the NotFound exception from rest_framwork.exceptions above

    def get(self, _request, pk):
        try:
            story = Story.objects.get(pk=pk)
            serialized_story = PopulatedStorySerializer(story)
            return Response(serialized_story.data, status=status.HTTP_200_OK)
        except Story.DoesNotExist:
            raise NotFound(detail="Can't find that story!") # <-- import the NotFound exception from rest_framwork.exceptions
        
    # Updating story with put method request
    def put(self, request, pk):
        story_to_update = self.get_story(pk=pk)
        if story_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_story = StorySerializer(story_to_update, data=request.data)
        if updated_story.is_valid():
            updated_story.save()
            return Response(updated_story.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_story.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Deleting story with delete request
    def delete(self, request, pk):
        story_to_delete = self.get_story(pk=pk)

        if story_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        story_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    
   # tested all stories routes in Postman - all successfull (FULL CRUD FOR STORIES) 