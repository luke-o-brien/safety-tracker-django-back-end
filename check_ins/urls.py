from django.urls import path
from .views import Check_InListView, Check_InDetailView

urlpatterns = [
  path('', Check_InListView.as_view()),
  path('<int:pk>/', Check_InDetailView.as_view()),
]
