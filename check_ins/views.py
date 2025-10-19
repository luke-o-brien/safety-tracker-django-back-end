# Imports
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes
from rest_framework.exceptions import NotFound

from .models import Check_In
from .serializers.common import Check_InSerializer
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
   
        