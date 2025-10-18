from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound
from rest_framework import status

from .models import Comment
from .serializers.common import CommentSerializer
from rest_framework.permissions import IsAuthenticated

class CommentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("CREATING COMMMENT USER ID", request.user.id)
        request.data["owner"] = request.user.id
        comment_to_add = CommentSerializer(data=request.data)
        try:
            comment_to_add.is_valid()
            comment_to_add.save()
            return Response(comment_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated,) # only get here if you are signed in

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Can't find that comment")

    def get(self, request, pk):
        comment = self.get_comment(pk=pk)
        serialized_comment = CommentSerializer(comment)
        return Response(serialized_comment.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment_to_update = self.get_comment(pk=pk)

        # request has been through the authentication process. It started as request.
        # request was sent with a token.
        #  token was checked, and the user was found.
        #  user was added to the request.
        if comment_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_comment = CommentSerializer(comment_to_update, data=request.data)

        if updated_comment.is_valid():
            updated_comment.save()
            return Response(updated_comment.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, request, pk):
        comment_to_delete = self.get_comment(pk=pk)

        if comment_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        comment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# tested comments routes via postman & all is working
