from .serializers import UserDetailSerializer
from .models import User
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_landlord(request, pk):
    user = User.objects.get(id = pk)
    if user or user is not None:
        serializers = UserDetailSerializer(user, many=False)
        print(serializers.data)

        return JsonResponse({'success' : serializers.data}, safe= False)
    else:
        return JsonResponse({'errors' : "User not found"}, safe= False)