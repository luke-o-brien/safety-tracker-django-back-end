from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound # This provides a default response for a not found

from .models import Author
from .serializers.common import AuthorSerializer
from .serializers.populated import PopulatedAuthorSerializer


# Creating views here

class AuthorListView(APIView):

    # handle a GET request in the AuthorListView
    def get(self, _request):
        # go to the database and get all the authors
        authors = Author.objects.all()
        serialized_authors = AuthorSerializer(authors, many=True)
        # return the serialized data and a 200 status code
        return Response(serialized_authors.data, status=status.HTTP_200_OK)
    
    # POST request
    def post(self, request):
        author_to_add = AuthorSerializer(data=request.data)
        try:
           author_to_add.is_valid()
           author_to_add.save()
           return Response(author_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AuthorDetailView(APIView):

    # for single author get, put and delete requests
    def get_author(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise NotFound(detail="Can't find that author!")

    def get(self, request, pk):
        author = self.get_author(pk=pk)
        serialized_author = PopulatedAuthorSerializer(author)
        return Response(serialized_author.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        author_to_update = self.get_author(pk=pk)
        updated_author = AuthorSerializer(author_to_update, data=request.data)

        if updated_author.is_valid():
            updated_author.save()
            return Response(updated_author.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_author.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        author_to_delete = self.get_author(pk=pk)
        author_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    

    # CRUD functionality for authors tested via POSTMAN & fully working!
    