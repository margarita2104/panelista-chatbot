from chatbot.views import ChatbotCreateListView, ChatbotDetailView
from django.urls import path

urlpatterns = [
    path('', ChatbotCreateListView.as_view(), name='chatbot-list-create'),
    path('<int:pk>/', ChatbotDetailView.as_view(), name='chatbot-detail'),
]