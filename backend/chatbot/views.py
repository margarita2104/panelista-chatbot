from rest_framework import generics, status
from rest_framework.response import Response

from .app import suggest_speakers_from_user_input
from .models import Chatbot
from .serializers import ChatbotSerializer


class ChatbotCreateListView(generics.ListCreateAPIView):
    serializer_class = ChatbotSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_prompt = serializer.validated_data.get('user_prompt')

        if user_prompt:
            chatbot_response = suggest_speakers_from_user_input(user_prompt)
            serializer.save(chatbot_response=chatbot_response)
        else:
            return Response({"error": "User prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatbotDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatbotSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        chatbot_entry = self.get_object()
        self.perform_destroy(chatbot_entry)
        return Response(status=status.HTTP_204_NO_CONTENT)
