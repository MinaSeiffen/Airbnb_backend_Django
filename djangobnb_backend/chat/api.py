from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailsSerializer

@api_view(['GET'])
def conversations_list(request):
    if request.user.is_anonymous:
        return JsonResponse({'error': 'Please, Login First'})
    serializer = ConversationListSerializer(request.user.conversations.all(), many= True)

    return JsonResponse({'success': serializer.data}, safe= False)


@api_view(['GET'])
def conversations_detail(request, pk):
    conversation = request.user.conversations.get(pk= pk)

    conversation_serializer = ConversationDetailsSerializer(conversation, many= False)

    return JsonResponse({'success': conversation_serializer.data}, safe= False)