from rest_framework import serializers

from chatbot.models import Chatbot


class ChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbot
        fields = ['id', 'user_prompt', 'chatbot_response', 'created_at']
        read_only_fields = ['id', 'created_at']
