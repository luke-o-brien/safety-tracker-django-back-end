# Imports
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Check_In
from .serializers import Check_InSerializer


# Create your views here
# Building out views.py to return all data eg. ListView
class Check_InListView(APIView):

  def get(self, _request):
    check_ins = Check_In.objects.all()
    serialized_check_ins = Check_InSerializer(check_ins, many=True)
    return Response(serialized_check_ins.data, status=status.HTTP_200_OK)
  
  