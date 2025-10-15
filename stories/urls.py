from django.urls import path
from .views import StoryListView

urlpatterns = [
  path('', StoryListView.as_view()),
]
