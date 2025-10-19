from django.urls import path
from .views import Check_InListView

urlpatterns = [
  path('', Check_InListView.as_view()),
]
