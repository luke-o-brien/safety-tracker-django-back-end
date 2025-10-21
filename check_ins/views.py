# Imports
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes
from rest_framework.exceptions import NotFound

from .models import Check_In
from .serializers.common import Check_InSerializer
from .serializers.populated import PopulatedCheck_InSerializer 
from rest_framework.permissions import IsAuthenticated


# Create your views here
# Building out views.py to return all data eg. ListView
class Check_InListView(APIView):
  permission_classes = (IsAuthenticated, )
  # GET request in the Check_InListView
  def get(self, _request):
    # Only show check-ins that belong to the logged-in user
    check_ins = Check_In.objects.filter(owner=_request.user)
    serialized_check_ins = Check_InSerializer(check_ins, many=True)
    return Response(serialized_check_ins.data, status=status.HTTP_200_OK)
  
  def post(self, _request):
        _request.data["owner"] = _request.user.id
        check_in_to_add = Check_InSerializer(data=_request.data)
        try:
           check_in_to_add.is_valid(raise_exception=True)
           check_in_to_add.save()
           return Response(check_in_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   
class Check_InDetailView(APIView):
    permission_classes = (IsAuthenticated, ) # sets the permission levels of the specific view by passing in the rest framework authentication class

    # custom method to retrieve a check_in from the DB and error if it's not found
    def get_check_in(self, pk):
        try:
            return Check_In.objects.get(pk=pk)
        except Check_In.DoesNotExist:
            raise NotFound(detail="Can't find that check_in") # <-- import the NotFound exception from rest_framwork.exceptions

    def get(self, _request, pk):
        try:
            check_in = Check_In.objects.get(pk=pk)
            # now only the user can see their own check_in
            if check_in.owner != _request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serialized_check_in = PopulatedCheck_InSerializer(check_in)
            return Response(serialized_check_in.data, status=status.HTTP_200_OK)
        except Check_In.DoesNotExist:
            raise NotFound(detail="Can't find that check_in") # <-- import the NotFound exception from rest_framwork.exceptions

    def put(self, request, pk):
        check_in_to_update = self.get_check_in(pk=pk)
        if check_in_to_update.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        updated_check_in = Check_InSerializer(check_in_to_update, data=request.data)
        if updated_check_in.is_valid():
            updated_check_in.save()
            return Response(updated_check_in.data, status=status.HTTP_202_ACCEPTED)

        return Response(updated_check_in.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        check_in_to_delete = self.get_check_in(pk=pk)

        if check_in_to_delete.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        check_in_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

    # check_ins - full CRUD functionality tested in POSTMAN
    # check_ins addtl - populated serializer added & now full backend is currently working with 5 data entities - for stretch goals, will add more in the future.
    