from django.urls import path

from backend.user.views import ListCreateUsersView, RetrieveUpdateDestroyUsersView

urlpatterns = [
    path('create/', ListCreateUsersView.as_view()),
    path('edit/<int:pk>/', RetrieveUpdateDestroyUsersView.as_view()),
]
